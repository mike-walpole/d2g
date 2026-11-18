<script>
	import {
		Button,
		TextInput,
		TextArea,
		Select,
		SelectItem,
		ComboBox,
		Checkbox,
		Grid,
		Column,
		Tile,
		Loading,
		InlineNotification
	} from 'carbon-components-svelte';
	// Removed carbon icons to avoid import issues
	import {
		t,
		cargoTypes,
		referralSources,
		apiBaseUrl,
		currentLanguage,
		configData
	} from '$lib/stores/config.js';
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { initAnalytics, setAnalyticsLanguage, track } from '$lib/analytics.js';

	// Responsive form handling
	let innerWidth = 0;

	// Form schema from AWS
	let formSchema = null;

	// Form state - will be dynamically initialized from schema
	let formData = {};

	let isSubmitting = false;
	let submitMessage = '';
	let submitStatus = 'info'; // 'success', 'error', 'info'

	// CAPTCHA DISABLED: Uncomment to re-enable Cloudflare Turnstile
	// let captchaToken = '';
	// let captchaWidget = null;

	// Select all checkboxes functionality
	let selectAllConsent = false;

	// List of consent checkboxes that should be controlled by select all
	const consentCheckboxIds = ['privacy_consent', 'terms_consent', 'cross_border_consent'];

	// Field validation state
	let fieldErrors = {};
	let fieldTouched = {};
	let showValidation = false;

	// Multilingual validation messages
	const validationMessages = {
		en: {
			required: 'This field is required',
			email: 'Please enter a valid email address',
			phone: 'Please enter a valid phone number',
			minLength: 'Please enter at least {min} characters',
			custom_prefix: 'Please enter a valid phone prefix (e.g., +33)',
			select: 'Please select an option',
			checkbox: 'This checkbox must be checked'
		},
		zh: {
			required: '此字段为必填项',
			email: '请输入有效的电子邮箱地址',
			phone: '请输入有效的电话号码',
			minLength: '请至少输入{min}个字符',
			custom_prefix: '请输入有效的电话区号（例如：+33）',
			select: '请选择一个选项',
			checkbox: '必须勾选此复选框'
		}
	};

	// Get validation message for field
	const getValidationMessage = (field, errorType, params = {}) => {
		const messages = validationMessages[$currentLanguage] || validationMessages.en;
		let message = messages[errorType] || messages.required;

		// Replace placeholders
		Object.keys(params).forEach((key) => {
			message = message.replace(`{${key}}`, params[key]);
		});

		return message;
	};

	// Validate individual field
	const validateField = (field) => {
		if (!field) return null;

		const value = formData[field.id];
		const isRequired = field.required || field.id === 'referral_source';

		// Check if field is empty
		const isEmpty = !value || (typeof value === 'string' && value.trim() === '');

		if (isRequired && isEmpty) {
			if (field.type === 'checkbox') {
				return getValidationMessage(field, 'checkbox');
			} else if (field.type === 'select') {
				return getValidationMessage(field, 'select');
			} else {
				return getValidationMessage(field, 'required');
			}
		}

		// Custom phone prefix validation
		if (field.id === 'custom_phone_prefix' && formData.phone_prefix === 'custom' && value) {
			if (!field.validation?.pattern || !new RegExp(field.validation.pattern).test(value)) {
				return getValidationMessage(field, 'custom_prefix');
			}
		}

		// Email validation
		if (field.type === 'email' && value && field.validation?.pattern) {
			if (!new RegExp(field.validation.pattern).test(value)) {
				return getValidationMessage(field, 'email');
			}
		}

		// Phone validation
		if (field.id === 'phone' && value && field.validation?.pattern) {
			if (!new RegExp(field.validation.pattern).test(value)) {
				return getValidationMessage(field, 'phone');
			}
		}

		// Min length validation
		if (field.validation?.minLength && value && value.length < field.validation.minLength) {
			return getValidationMessage(field, 'minLength', { min: field.validation.minLength });
		}

		return null;
	};

	// Validate all fields
	const validateAllFields = () => {
		const errors = {};

		formSchema?.fields?.forEach((field) => {
			// Skip custom_phone_prefix unless phone_prefix is 'custom'
			if (field.id === 'custom_phone_prefix' && formData.phone_prefix !== 'custom') {
				return;
			}

			const error = validateField(field);
			if (error) {
				errors[field.id] = error;
			}
		});

		// Special case: custom phone prefix validation
		if (formData.phone_prefix === 'custom') {
			const customField = formSchema?.fields?.find((f) => f.id === 'custom_phone_prefix');
			if (customField) {
				const error = validateField(customField);
				if (error) {
					errors['custom_phone_prefix'] = error;
				}
			}
		}

		fieldErrors = errors;
		return Object.keys(errors).length === 0;
	};

	// Helper function to get localized text from schema (reactive)
	$: getLocalizedText = (textObj, fallback = '') => {
		if (!textObj) return fallback;
		if (typeof textObj === 'string') return textObj;
		return textObj[$currentLanguage] || textObj.en || fallback;
	};

	// Helper function to get field by id (reactive)
	$: getField = (fieldId) => {
		if (!formSchema?.fields) return null;
		return formSchema.fields.find((field) => field.id === fieldId);
	};

	// Country code to phone prefix mapping
	const countryToPhonePrefix = {
		CN: '+86', // China
		HK: '+852', // Hong Kong
		MO: '+853', // Macau
		TW: '+886', // Taiwan
		JP: '+81', // Japan
		KR: '+82', // South Korea
		IN: '+91', // India
		MY: '+60', // Malaysia
		TH: '+66', // Thailand
		VN: '+84' // Vietnam
	};

	// Initialize form data from schema
	function initializeFormData() {
		if (!formSchema?.fields) return;

		// Determine default phone prefix based on geolocation
		const geolocation = $page.data?.geolocation;
		const country = geolocation?.country?.toUpperCase();
		const defaultPhonePrefix = countryToPhonePrefix[country] || '+48'; // Default to Poland
		console.log('📍 Phone prefix based on geolocation:', {
			country,
			defaultPhonePrefix
		});

		const newFormData = {};
		formSchema.fields.forEach((field) => {
			if (field.type === 'checkbox') {
				newFormData[field.id] = false;
			} else if (field.type === 'select' && field.id === 'phone_prefix') {
				newFormData[field.id] = defaultPhonePrefix;
			} else if (field.type === 'select') {
				// Other select fields (cargo_type, referral_source) start empty
				newFormData[field.id] = '';
			} else {
				newFormData[field.id] = '';
			}
		});

		formData = newFormData;
		console.log('📝 Frontend: Form data initialized:', formData);
	}

	// Load form schema - fetch from DynamoDB only once when page loads
	async function loadFormSchema() {
		try {
			console.log('🔄 Frontend: Fetching schema from DynamoDB...');
			const apiUrl = await new Promise((resolve) => {
				apiBaseUrl.subscribe((url) => resolve(url))();
			});

			const response = await fetch(`${apiUrl}/schema?formId=dock2gdansk-main`);
			const data = await response.json();

			if (data.success) {
				formSchema = data.schema;
				console.log('✅ Frontend: Schema loaded from DynamoDB:', formSchema);
				console.log('📊 Frontend: Schema version:', formSchema?.version || 'unknown');
				console.log('📊 Frontend: Number of fields:', formSchema?.fields?.length || 0);
				console.log('🌐 Frontend: Current language:', $currentLanguage);

				// Debug: Check if referral_source field is required
				const referralField = formSchema?.fields?.find((f) => f.id === 'referral_source');
				console.log('🔍 Referral source field:', referralField);
				console.log('🔍 Referral source required:', referralField?.required);

				// Initialize form data with new schema
				initializeFormData();
			} else {
				console.error('❌ Frontend: Failed to load form schema:', data.error);
				formSchema = null;
			}
		} catch (error) {
			console.error('💥 Frontend: Error loading form schema:', error);
			formSchema = null;
		}
	}

	// Reactive translations for hero section with direct language support
	$: heroTitle =
		$currentLanguage === 'zh'
			? '您值得信赖的国际货运合作伙伴'
			: 'Your Trusted Partner for International Cargo Transportation to Poland';
	$: heroSubtitle =
		$currentLanguage === 'zh'
			? '可靠、高效、专业的运输服务，连接全球市场与中东欧地区'
			: 'Reliable, efficient, and professional shipping services that connect global markets to Central and Eastern Europe';

	// CAPTCHA DISABLED: Uncomment to re-enable Cloudflare Turnstile
	// Define CAPTCHA callbacks globally before onMount
	// globalThis.handleTurnstileSuccess = (token) => {
	// 	captchaToken = token;
	// 	console.log('✅ CAPTCHA completed with token:', token);
	// };

	// globalThis.handleTurnstileError = (error) => {
	// 	captchaToken = '';
	// 	console.error('❌ CAPTCHA error:', error);
	// 	console.error('Error details:', {
	// 		error,
	// 		siteKey: '0x4AAAAAAB12UeOd4h-pzqW1',
	// 		domain: window.location.hostname
	// 	});
	// };

	// globalThis.handleTurnstileExpired = () => {
	// 	captchaToken = '';
	// 	console.log('⏰ CAPTCHA expired');
	// };

	onMount(() => {
		initAnalytics({
			country: $page.data?.geolocation?.country,
			language: $currentLanguage
		});
		const formEl = document.getElementById('inquiry-form');
		const observer = new IntersectionObserver(
			(entries) => {
				if (!formViewed && entries.some((en) => en.isIntersecting)) {
					formViewed = true;
					track('form_viewed');
					observer.disconnect();
				}
			},
			{ threshold: 0.2 }
		);
		if (formEl) observer.observe(formEl);
		// pagehide fires on tab close, navigation away and mobile backgrounding
		window.addEventListener('pagehide', sendAbandon);
		return () => {
			observer.disconnect();
			window.removeEventListener('pagehide', sendAbandon);
		};
	});

	onMount(async () => {
		// CAPTCHA DISABLED: Uncomment to re-enable Cloudflare Turnstile
		// Debug: Check if Turnstile is loaded and render widget
		// const checkTurnstile = () => {
		// 	if (window.turnstile) {
		// 		console.log('✅ Turnstile API loaded successfully');

		// 		// Explicitly render the widget
		// 		try {
		// 			window.turnstile.render('#turnstile-widget', {
		// 				sitekey: '0x4AAAAAAB12UeOd4h-pzqW1',
		// 				callback: (token) => {
		// 					captchaToken = token;
		// 					console.log('✅ CAPTCHA completed with token:', token);
		// 				},
		// 				'error-callback': (error) => {
		// 					captchaToken = '';
		// 					console.error('❌ CAPTCHA error:', error);
		// 				},
		// 				'expired-callback': () => {
		// 					captchaToken = '';
		// 					console.log('⏰ CAPTCHA expired');
		// 				},
		// 				theme: 'light'
		// 			});
		// 			console.log('✅ Turnstile widget rendered explicitly');
		// 		} catch (error) {
		// 			console.error('❌ Failed to render Turnstile widget:', error);
		// 		}
		// 	} else {
		// 		console.log('⏳ Waiting for Turnstile API to load...');
		// 		setTimeout(checkTurnstile, 1000);
		// 	}
		// };

		// Check immediately and then wait if needed
		// setTimeout(checkTurnstile, 100);

		// Debug CAPTCHA token state
		// setInterval(() => {
		// 	console.log('🔍 CAPTCHA token status:', {
		// 		captchaToken,
		// 		hasToken: !!captchaToken,
		// 		buttonDisabled: !captchaToken
		// 	});
		// }, 5000);

		// Load config data and schema in parallel for faster loading
		const configModule = await import('$lib/stores/config.js');

		// Start both loads simultaneously (parallel, not sequential)
		const [configResult, schemaResult] = await Promise.allSettled([
			configModule.loadConfig($currentLanguage),
			loadFormSchema()
		]);

		if (configResult.status === 'fulfilled') {
			console.log('✅ Config data loaded');
		} else {
			console.error('❌ Config loading failed:', configResult.reason);
		}

		if (schemaResult.status === 'fulfilled') {
			console.log('✅ Schema loaded');
		} else {
			console.error('❌ Schema loading failed:', schemaResult.reason);
		}
	});

	async function handleSubmit() {
		// Show validation and validate all fields
		showValidation = true;
		const isValid = validateAllFields();
		track('submit_clicked', {
			valid: isValid,
			error_fields: Object.keys(fieldErrors),
			ms_since_start: formStartedAt ? Date.now() - formStartedAt : null
		});

		if (!isValid) {
			// Find the first error field and scroll to it
			const firstErrorField = Object.keys(fieldErrors)[0];
			const element = document.getElementById(firstErrorField);
			if (element) {
				element.scrollIntoView({ behavior: 'smooth', block: 'center' });
			}

			submitMessage =
				$currentLanguage === 'zh' ? '请填写所有必填字段' : 'Please fill in all required fields';
			submitStatus = 'error';
			return;
		}

		// CAPTCHA DISABLED: Uncomment to re-enable Cloudflare Turnstile
		// Check CAPTCHA token
		// if (!captchaToken) {
		// 	submitMessage =
		// 		$currentLanguage === 'zh' ? '请完成验证码验证' : 'Please complete the CAPTCHA verification';
		// 	submitStatus = 'error';
		// 	return;
		// }

		isSubmitting = true;
		submitMessage = '';

		try {
			const apiUrl = await new Promise((resolve) => {
				apiBaseUrl.subscribe((url) => resolve(url))();
			});

			const response = await fetch(`${apiUrl}/submit-form`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					form_data: formData,
					user_email: formData.email,
					form_id: 'dock2gdansk-main',
					schema_version: formSchema?.version
					// CAPTCHA DISABLED: Uncomment to re-enable Cloudflare Turnstile
					// captcha_token: captchaToken
				})
			});

			const result = await response.json();

			if (result.success) {
				formSubmitted = true;
				track('form_submitted', {
					...cargoProps(),
					ms_since_start: formStartedAt ? Date.now() - formStartedAt : null
				});
				// Success message
				const successMessages = {
					en: 'Thank you! Your inquiry has been submitted successfully.',
					zh: '谢谢！您的询盘已成功提交。'
				};

				submitMessage = successMessages[$currentLanguage] || successMessages.en;
				submitStatus = 'success';

				// Reset form and validation state
				formData = {};
				fieldErrors = {};
				fieldTouched = {};
				showValidation = false;
				// CAPTCHA DISABLED: Uncomment to re-enable Cloudflare Turnstile
				// captchaToken = '';
				// if (captchaWidget) {
				// 	window.turnstile?.reset(captchaWidget);
				// }
				initializeFormData();
			} else {
				track('form_submit_failed', {
					http_status: response.status,
					error: result.error || 'unknown',
					error_fields: Object.keys(result.field_errors || {})
				});
				throw new Error(result.error || 'Submission failed');
			}
		} catch (error) {
			console.error('Submission error:', error);

			const errorMessages = {
				en: 'An error occurred. Please try again.',
				zh: '发生错误，请重试。'
			};

			submitMessage = errorMessages[$currentLanguage] || errorMessages.en;
			submitStatus = 'error';
		} finally {
			isSubmitting = false;
		}
	}

	// ---------- Form analytics (no field values are ever sent) ----------
	// Unit of analysis = one page load. Question being answered: does the long cargo list cause drop-off?
	let formViewed = false;
	let formStartedAt = 0;
	let formSubmitted = false;
	let abandonSent = false;
	let lastField = null;
	const completedFields = new Set();
	let cargoFirstFocusAt = 0;
	let cargoFocusCount = 0;
	let cargoChangeCount = 0;

	function fieldIndex(id) {
		return formSchema?.fields?.findIndex((f) => f.id === id) ?? -1;
	}

	function cargoProps(id = formData.cargo_type) {
		if (!id) return { cargo_type: null };
		const list = $cargoTypes;
		const idx = list.findIndex((c) => c.id === id);
		return {
			cargo_type: id,
			cargo_name: idx >= 0 ? list[idx].name : id,
			cargo_maps_to_others: idx >= 0 ? list[idx].mapsTo === 'others' || id === 'others' : null,
			cargo_list_position: idx >= 0 ? idx + 1 : null,
			cargo_list_length: list.length
		};
	}

	// Read the DOM element, not formData: Carbon's bind:selected propagates after this handler runs.
	function isFilled(el) {
		if (el.type === 'checkbox') return el.checked;
		return typeof el.value === 'string' && el.value.trim() !== '';
	}

	function markStarted(id) {
		if (formStartedAt) return;
		formStartedAt = Date.now();
		track('form_started', { first_field: id });
	}

	function handleFormFocusIn(e) {
		const id = e.target?.id;
		if (!id || fieldIndex(id) < 0) return;
		markStarted(id);
		lastField = id;
		if (id === 'cargo_type') {
			cargoFocusCount += 1;
			if (!cargoFirstFocusAt) {
				cargoFirstFocusAt = Date.now();
				track('cargo_focused', { cargo_list_length: $cargoTypes.length });
			}
		}
	}

	function handleFormFieldDone(e) {
		const id = e.target?.id;
		if (!id || fieldIndex(id) < 0) return;
		// The cargo combobox input holds the typed search text, not the selected id: tracked in handleCargoSelect.
		if (id === 'cargo_type') return;
		if (e.type === 'change') markStarted(id);
		if (!completedFields.has(id) && isFilled(e.target)) {
			completedFields.add(id);
			track('field_completed', { field: id, field_index: fieldIndex(id) + 1 });
		}
	}

	// Cargo combobox: typing filters the list ("c" -> Coal, Container, ...).
	let cargoQuery = '';
	let cargoSearchUsed = false;
	$: cargoAll = $cargoTypes.map((c) => ({ id: c.id, text: c.name }));
	$: if (cargoQuery && !cargoAll.some((i) => i.text === cargoQuery)) cargoSearchUsed = true;

	/** 0 = name starts with query, 1 = a word starts with it, 2 = contains it (3+ chars), 9 = no match */
	function cargoRank(item, value) {
		const q = (value ?? '').trim().toLowerCase();
		if (!q) return 0;
		// Reopening a filled field shows the whole list, not just the current pick
		const picked = cargoAll.find((i) => i.id === formData.cargo_type);
		if (picked && picked.text.toLowerCase() === q) return 0;
		const name = item.text.toLowerCase();
		if (name.startsWith(q)) return 0;
		if (name.split(/[\s/(),+-]+/).some((w) => w.startsWith(q))) return 1;
		return q.length >= 3 && name.includes(q) ? 2 : 9;
	}
	// "Others" always stays available, at the end
	const cargoMatches = (item, value) => item.id === 'others' || cargoRank(item, value) < 9;
	$: cargoItems = [...cargoAll].sort(
		(a, b) =>
			(a.id === 'others') - (b.id === 'others') ||
			cargoRank(a, cargoQuery) - cargoRank(b, cargoQuery)
	);

	function validateCargo(field) {
		fieldTouched[field.id] = true;
		const error = validateField(field);
		if (error) fieldErrors[field.id] = error;
		else delete fieldErrors[field.id];
		fieldErrors = fieldErrors;
	}

	function handleCargoSelect(field, e) {
		const id = e.detail?.selectedId;
		if (!id) return;
		formData[field.id] = id;
		validateCargo(field);
		markStarted(field.id);
		cargoChangeCount += 1;
		track('cargo_selected', {
			...cargoProps(id),
			ms_to_select: cargoFirstFocusAt ? Date.now() - cargoFirstFocusAt : null,
			focus_count: cargoFocusCount,
			change_count: cargoChangeCount,
			used_search: cargoSearchUsed
		});
		cargoSearchUsed = false;
		if (!completedFields.has(field.id)) {
			completedFields.add(field.id);
			track('field_completed', { field: field.id, field_index: fieldIndex(field.id) + 1 });
		}
	}

	function sendAbandon() {
		if (!formStartedAt || formSubmitted || abandonSent) return;
		abandonSent = true;
		track(
			'form_abandoned',
			{
				last_field: lastField,
				last_field_index: lastField ? fieldIndex(lastField) + 1 : null,
				fields_completed: completedFields.size,
				reached_cargo: cargoFirstFocusAt > 0,
				cargo_selected: Boolean(formData.cargo_type),
				ms_since_start: Date.now() - formStartedAt
			},
			{ beacon: true }
		);
	}

	$: setAnalyticsLanguage($currentLanguage);

	// Handle select all consent checkboxes
	function handleSelectAllConsent() {
		consentCheckboxIds.forEach((id) => {
			if (formData[id] !== undefined) {
				formData[id] = selectAllConsent;
			}
		});
	}

	// Update select all state when individual checkboxes change
	$: {
		if (formData && consentCheckboxIds.length > 0) {
			const allChecked = consentCheckboxIds.every((id) => formData[id] === true);
			const anyChecked = consentCheckboxIds.some((id) => formData[id] === true);

			if (allChecked) {
				selectAllConsent = true;
			} else if (!anyChecked) {
				selectAllConsent = false;
			}
		}
	}
</script>

<svelte:window bind:innerWidth />

<svelte:head>
	<title
		>{t('site_title', 'Port Gdańsk Connect')} - {t(
			'site_tagline',
			'Professional Cargo Transportation'
		)}</title
	>
</svelte:head>

<!-- Hero Section -->
<section
	style="background-image: url('/hero.avif'); background-size: cover; background-position: center; background-repeat: no-repeat; color: white; padding: 120px 0 64px 0; margin-top: 48px; position: relative;"
>
	<!-- Dark overlay for better text readability -->
	<div
		style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0, 67, 206, 0.7);"
	></div>

	<div
		style="max-width: 1200px; margin: 0 auto; padding: 0 16px; text-align: center; position: relative; z-index: 1;"
	>
		<!-- Centered logo -->
		<img
			src="/logo.png"
			alt="Port of Gdańsk Logo"
			style="height: 360px; width: auto; margin: 0 auto 40px auto; display: block;"
		/>

		<h1 style="font-size: 48px; font-weight: normal; margin-bottom: 16px; line-height: 1.2;">
			{heroTitle}
		</h1>
		<p
			style="font-size: 20px; margin-bottom: 32px; max-width: 800px; margin-left: auto; margin-right: auto;"
		>
			{heroSubtitle}{$currentLanguage === 'zh'
				? ' — 由格但斯克港提供'
				: ' – delivered by Port of Gdańsk.'}
		</p>
	</div>
</section>

<!-- Form Section -->
<section id="inquiry-form" class="form-section">
	<div class="form-wrapper">
		<div class="form-container">
			<h2 style="font-size: 32px; font-weight: bold; margin-bottom: 8px; text-align: center;">
				{formSchema
					? getLocalizedText(formSchema.title, 'Submit Your Inquiry')
					: t('form.title', 'Submit Your Inquiry')}
			</h2>
			<p style="color: #666; margin-bottom: 32px; text-align: center;">
				{formSchema
					? getLocalizedText(formSchema.description, 'Fill out the form below')
					: t('form.description', 'Fill out the form below')}
			</p>

			<form
				on:submit|preventDefault={handleSubmit}
				on:focusin={handleFormFocusIn}
				on:focusout={handleFormFieldDone}
				on:change={handleFormFieldDone}
				class="space-y-6"
			>
				<Grid condensed>
					{#if formSchema?.fields}
						{#each formSchema.fields as field, index}
							<!-- Add Select All checkbox after inquiry_content and before consent checkboxes -->
							{#if field.id === 'privacy_consent' && formSchema.fields.some( (f) => consentCheckboxIds.includes(f.id) )}
								<Column sm={4} md={8} lg={16}>
									<div
										style="margin-bottom: 24px; padding: 16px; background-color: #f0f8ff; border: 2px dashed #0066cc; border-radius: 8px;"
									>
										<Checkbox
											labelText={$currentLanguage === 'zh'
												? '选择所有必需的同意条款'
												: 'Select all required consents'}
											bind:checked={selectAllConsent}
											on:change={handleSelectAllConsent}
										/>
										<p style="margin: 8px 0 0 0; font-size: 12px; color: #666; font-style: italic;">
											{$currentLanguage === 'zh'
												? '选中此框可一次性选择所有同意条款复选框'
												: 'Check this box to select all consent checkboxes at once'}
										</p>
									</div>
								</Column>
							{/if}

							<!-- Skip custom_phone_prefix field in main loop - handled separately -->
							{#if field.id !== 'custom_phone_prefix'}
								<Column sm={4} md={8} lg={16}>
									<div style="margin-bottom: 24px;">
										{#if field.type === 'text' || field.type === 'email' || field.type === 'tel'}
											<TextInput
												id={field.id}
												type={field.type}
												labelText={getLocalizedText(field.label, field.id) +
													(field.required || field.id === 'referral_source' ? ' *' : '')}
												placeholder={field.placeholder
													? getLocalizedText(field.placeholder, '')
													: ''}
												bind:value={formData[field.id]}
												invalid={showValidation && fieldErrors[field.id]}
												invalidText={fieldErrors[field.id]}
												on:blur={() => {
													fieldTouched[field.id] = true;
													const error = validateField(field);
													if (error) {
														fieldErrors[field.id] = error;
													} else {
														delete fieldErrors[field.id];
													}
													fieldErrors = fieldErrors; // trigger reactivity
												}}
											/>
										{:else if field.type === 'textarea'}
											<TextArea
												id={field.id}
												labelText={getLocalizedText(field.label, field.id) +
													(field.required || field.id === 'referral_source' ? ' *' : '')}
												placeholder={field.placeholder
													? getLocalizedText(field.placeholder, '')
													: ''}
												bind:value={formData[field.id]}
												rows={field.rows || 4}
												invalid={showValidation && fieldErrors[field.id]}
												invalidText={fieldErrors[field.id]}
												on:blur={() => {
													fieldTouched[field.id] = true;
													const error = validateField(field);
													if (error) {
														fieldErrors[field.id] = error;
													} else {
														delete fieldErrors[field.id];
													}
													fieldErrors = fieldErrors; // trigger reactivity
												}}
											/>
										{:else if field.type === 'select' && field.id === 'cargo_type'}
											<ComboBox
												id={field.id}
												titleText={getLocalizedText(field.label, field.id) +
													(field.required ? ' *' : '')}
												placeholder={$currentLanguage === 'zh'
													? '输入或选择货物类型'
													: 'Type or select cargo type'}
												items={cargoItems}
												shouldFilterItem={cargoMatches}
												bind:selectedId={formData[field.id]}
												bind:value={cargoQuery}
												invalid={showValidation && fieldErrors[field.id]}
												invalidText={fieldErrors[field.id]}
												on:select={(e) => handleCargoSelect(field, e)}
												on:clear={() => validateCargo(field)}
											/>
										{:else if field.type === 'select'}
											<Select
												id={field.id}
												labelText={getLocalizedText(field.label, field.id) +
													(field.required || field.id === 'referral_source' ? ' *' : '')}
												placeholder={field.placeholder
													? getLocalizedText(field.placeholder, '')
													: ''}
												bind:selected={formData[field.id]}
												invalid={showValidation && fieldErrors[field.id]}
												invalidText={fieldErrors[field.id]}
												on:change={() => {
													fieldTouched[field.id] = true;
													const error = validateField(field);
													if (error) {
														fieldErrors[field.id] = error;
													} else {
														delete fieldErrors[field.id];
													}
													fieldErrors = fieldErrors; // trigger reactivity
												}}
											>
												{#if field.id === 'referral_source'}
													<!-- Add placeholder option for referral source -->
													<SelectItem
														value=""
														text={$currentLanguage === 'zh' ? '请选择' : 'Please select'}
														disabled
													/>
													{#each $referralSources as source}
														<SelectItem value={source.id} text={source.name} />
													{/each}
												{:else if field.options}
													{#each field.options as option}
														<SelectItem
															value={option.value}
															text={getLocalizedText(option.label, option.value)}
														/>
													{/each}
												{/if}
											</Select>
										{:else if field.type === 'checkbox'}
											{#if field.id === 'privacy_consent' || field.id === 'terms_consent' || field.id === 'cross_border_consent'}
												<!-- Custom checkbox with HTML support for privacy/terms/cross-border -->
												<div class="checkbox-wrapper" style="margin-bottom: 16px;">
													<input
														type="checkbox"
														id={field.id}
														bind:checked={formData[field.id]}
														style="margin-right: 8px;"
														class={showValidation && fieldErrors[field.id] ? 'error' : ''}
														on:change={() => {
															fieldTouched[field.id] = true;
															const error = validateField(field);
															if (error) {
																fieldErrors[field.id] = error;
															} else {
																delete fieldErrors[field.id];
															}
															fieldErrors = fieldErrors; // trigger reactivity
														}}
													/>
													<label
														for={field.id}
														style="font-size: 14px; cursor: pointer; color: {showValidation &&
														fieldErrors[field.id]
															? '#da1e28'
															: 'inherit'};"
													>
														{#if field.id === 'privacy_consent'}
															{@html 'I agree to the <a href="/terms" target="_blank" style="color: #0066cc; text-decoration: underline;">Terms of Use</a> and <a href="/privacy" target="_blank" style="color: #0066cc; text-decoration: underline;">Privacy Policy</a>.' +
																(field.required ? ' *' : '')}
														{:else if field.id === 'terms_consent'}
															{@html 'I explicitly consent to the sharing of my professional profile and contact information with other users of the platform for business matchmaking.' +
																(field.required ? ' *' : '')}
														{:else if field.id === 'cross_border_consent'}
															{@html 'I explicitly consent to the sharing of my data with third-party service providers (such as hosting and analytics companies) as described in the Privacy Policy.' +
																(field.required ? ' *' : '')}
														{:else}
															{@html (field.description
																? getLocalizedText(field.description, field.id)
																: getLocalizedText(field.label, field.id)) +
																(field.required ? ' *' : '')}
														{/if}
													</label>
													{#if showValidation && fieldErrors[field.id]}
														<div style="color: #da1e28; font-size: 12px; margin-top: 4px;">
															{fieldErrors[field.id]}
														</div>
													{/if}
												</div>
											{:else}
												<Checkbox
													id={field.id}
													labelText={(field.description
														? getLocalizedText(field.description, field.id)
														: getLocalizedText(field.label, field.id)) +
														(field.required ? ' *' : '')}
													bind:checked={formData[field.id]}
													invalid={showValidation && fieldErrors[field.id]}
													invalidText={fieldErrors[field.id]}
													on:change={() => {
														fieldTouched[field.id] = true;
														const error = validateField(field);
														if (error) {
															fieldErrors[field.id] = error;
														} else {
															delete fieldErrors[field.id];
														}
														fieldErrors = fieldErrors; // trigger reactivity
													}}
												/>
											{/if}
										{/if}
									</div>
								</Column>
							{/if}

							<!-- Show custom phone prefix field only when "custom" is selected -->
							{#if field.id === 'phone_prefix' && formData.phone_prefix === 'custom'}
								{#if formSchema?.fields.find((f) => f.id === 'custom_phone_prefix')}
									{@const customField = formSchema.fields.find(
										(f) => f.id === 'custom_phone_prefix'
									)}
									<Column sm={4} md={8} lg={16}>
										<div style="margin-bottom: 24px;">
											<TextInput
												id="custom_phone_prefix"
												type="text"
												labelText={getLocalizedText(customField.label, customField.id) + ' *'}
												placeholder={customField.placeholder
													? getLocalizedText(customField.placeholder, '')
													: ''}
												bind:value={formData.custom_phone_prefix}
												invalid={showValidation && fieldErrors.custom_phone_prefix}
												invalidText={fieldErrors.custom_phone_prefix}
												on:blur={() => {
													fieldTouched.custom_phone_prefix = true;
													const error = validateField(customField);
													if (error) {
														fieldErrors.custom_phone_prefix = error;
													} else {
														delete fieldErrors.custom_phone_prefix;
													}
													fieldErrors = fieldErrors; // trigger reactivity
												}}
											/>
										</div>
									</Column>
								{/if}
							{/if}
						{/each}
					{/if}

					<!-- CAPTCHA DISABLED: Uncomment to re-enable Cloudflare Turnstile -->
					<!-- <Column sm={4} md={8} lg={16}>
						<div style="margin-bottom: 24px; display: flex; justify-content: center;">
							<div id="turnstile-widget"></div>
						</div>
					</Column> -->

					<Column sm={4} md={8} lg={16}>
						<div class="submit-section">
							<!-- CAPTCHA DISABLED: Removed !captchaToken from disabled condition -->
							<Button type="submit" size="lg" disabled={isSubmitting}>
								{#if isSubmitting}
									<Loading withOverlay={false} small />
									{t('form.submitting', 'Submitting...')}
								{:else}
									{formSchema?.submitButton
										? getLocalizedText(formSchema.submitButton, 'Submit Inquiry')
										: t('form.submit', 'Submit Inquiry')}
								{/if}
							</Button>

							{#if submitMessage}
								<div class="confirmation-message">
									<InlineNotification kind={submitStatus} title={submitMessage} hideCloseButton />
								</div>
							{/if}
						</div>
					</Column>
				</Grid>
			</form>
		</div>
	</div>
</section>

<style>
	.form-section {
		padding: 64px 0;
		background: #f4f4f4;
	}

	.form-wrapper {
		max-width: 900px;
		margin: 0 auto;
		padding: 0 16px;
	}

	.form-container {
		background: #f9f9f9;
		border-radius: 8px;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
		padding: 48px;
	}

	.submit-section {
		display: flex;
		justify-content: center;
		align-items: center;
		gap: 16px;
		margin-top: 24px;
		flex-wrap: wrap;
	}

	.confirmation-message {
		flex: 1;
		min-width: 300px;
	}

	/* Mobile responsive adjustments */
	@media (max-width: 768px) {
		.form-section {
			padding: 32px 0;
		}

		.form-wrapper {
			padding: 0 8px;
		}

		.form-container {
			padding: 24px 16px;
			border-radius: 4px;
		}

		/* Ensure form takes full width on mobile */
		:global(.bx--col) {
			padding-left: 4px !important;
			padding-right: 4px !important;
		}

		/* Mobile form field adjustments */
		:global(.bx--text-input),
		:global(.bx--text-area),
		:global(.bx--select-input) {
			width: 100% !important;
			box-sizing: border-box !important;
		}

		/* Mobile grid adjustments */
		:global(.bx--grid) {
			margin-left: -4px !important;
			margin-right: -4px !important;
		}

		/* Mobile submit section adjustments */
		.submit-section {
			flex-direction: column;
			align-items: stretch;
		}

		.confirmation-message {
			min-width: auto;
			margin-top: 12px;
		}
	}

	/* Custom checkbox error styling */
	:global(input.error) {
		border-color: #da1e28 !important;
		outline-color: #da1e28 !important;
	}

	/* Required field indicator */
	:global(.bx--label:not(.bx--label--disabled)) {
		font-weight: 500;
	}

	/* Tablet adjustments */
	@media (max-width: 1024px) and (min-width: 769px) {
		.form-container {
			padding: 36px 24px;
		}
	}
</style>
