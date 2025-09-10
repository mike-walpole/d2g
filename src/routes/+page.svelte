<script>
	import { 
		Button, TextInput, TextArea, Select, SelectItem, Checkbox, 
		Grid, Column, Tile, Loading, InlineNotification 
	} from 'carbon-components-svelte';
	// Removed carbon icons to avoid import issues
	import { t, cargoTypes, apiBaseUrl, currentLanguage, configData } from '$lib/stores/config.js';
	import { onMount } from 'svelte';

	// Responsive form handling
	let innerWidth = 0;

	// Form schema from AWS
	let formSchema = null;

	// Form state - will be dynamically initialized from schema
	let formData = {};

	let isSubmitting = false;
	let submitMessage = '';
	let submitStatus = 'info'; // 'success', 'error', 'info'

	// Select all checkboxes functionality
	let selectAllConsent = false;
	
	// List of consent checkboxes that should be controlled by select all
	const consentCheckboxIds = ['privacy_consent', 'terms_consent', 'cross_border_consent'];

	// Helper function to get localized text from schema (reactive)
	$: getLocalizedText = (textObj, fallback = '') => {
		if (!textObj) return fallback;
		if (typeof textObj === 'string') return textObj;
		return textObj[$currentLanguage] || textObj.en || fallback;
	};

	// Helper function to get field by id (reactive)
	$: getField = (fieldId) => {
		if (!formSchema?.fields) return null;
		return formSchema.fields.find(field => field.id === fieldId);
	};

	// Initialize form data from schema
	function initializeFormData() {
		if (!formSchema?.fields) return;
		
		const newFormData = {};
		formSchema.fields.forEach(field => {
			if (field.type === 'checkbox') {
				newFormData[field.id] = false;
			} else if (field.type === 'select' && field.id === 'phone_prefix') {
				newFormData[field.id] = '+86'; // Keep default phone prefix
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
			const apiUrl = await new Promise(resolve => {
				apiBaseUrl.subscribe(url => resolve(url))();
			});

			const response = await fetch(`${apiUrl}/schema?formId=dock2gdansk-main`);
			const data = await response.json();

			if (data.success) {
				formSchema = data.schema;
				console.log('✅ Frontend: Schema loaded from DynamoDB:', formSchema);
				console.log('📊 Frontend: Schema version:', formSchema?.version || 'unknown');
				console.log('📊 Frontend: Number of fields:', formSchema?.fields?.length || 0);
				console.log('🌐 Frontend: Current language:', $currentLanguage);
				
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

	// Reactive translations for hero section - simplified to prevent loops
	$: currentTranslations = $configData?.translations?.[$currentLanguage] || $configData?.translations?.en || {};
	$: heroTitle = currentTranslations?.hero?.title || 'Your Trusted Partner for China-Poland Cargo Transportation';
	$: heroSubtitle = currentTranslations?.hero?.subtitle || 'Reliable, efficient, and professional shipping services connecting Asia to Europe';

	onMount(async () => {
		// Load config data first and wait for it
		const configModule = await import('$lib/stores/config.js');
		await configModule.loadConfig($currentLanguage);
		console.log('✅ Config data loaded');
		
		// Load schema once when page loads
		loadFormSchema();
	});

	async function handleSubmit() {
		// Validate required fields dynamically
		if (!formSchema?.fields) {
			submitMessage = t('form.error', 'Form schema not loaded');
			submitStatus = 'error';
			return;
		}
		
		// Check all required fields
		const missingFields = [];
		formSchema.fields.forEach(field => {
			if (field.required) {
				if (field.type === 'checkbox') {
					if (!formData[field.id]) {
						missingFields.push(getLocalizedText(field.label, field.id));
					}
				} else {
					if (!formData[field.id] || formData[field.id].trim() === '') {
						missingFields.push(getLocalizedText(field.label, field.id));
					}
				}
			}
		});
		
		if (missingFields.length > 0) {
			submitMessage = t('form.error', 'Please fill in all required fields') + ': ' + missingFields.join(', ');
			submitStatus = 'error';
			return;
		}

		isSubmitting = true;
		submitMessage = '';

		try {
			const apiUrl = await new Promise(resolve => {
				apiBaseUrl.subscribe(url => resolve(url))();
			});

			const response = await fetch(`${apiUrl}/submit-form`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					formData: formData,
					userEmail: formData.email,
					formId: 'dock2gdansk-main'
				})
			});

			const result = await response.json();

			if (result.success) {
				submitMessage = t('form.success', 'Thank you! Your inquiry has been submitted successfully.');
				submitStatus = 'success';
				
				// Reset form using current schema
				initializeFormData();
			} else {
				submitMessage = result.error || t('form.error', 'An error occurred. Please try again.');
				submitStatus = 'error';
			}
		} catch (error) {
			console.error('Submit error:', error);
			submitMessage = t('form.error', 'An error occurred. Please try again.');
			submitStatus = 'error';
		} finally {
			isSubmitting = false;
		}
	}
	
	// Handle select all consent checkboxes
	function handleSelectAllConsent() {
		consentCheckboxIds.forEach(id => {
			if (formData[id] !== undefined) {
				formData[id] = selectAllConsent;
			}
		});
	}
	
	// Update select all state when individual checkboxes change
	$: {
		if (formData && consentCheckboxIds.length > 0) {
			const allChecked = consentCheckboxIds.every(id => formData[id] === true);
			const anyChecked = consentCheckboxIds.some(id => formData[id] === true);
			
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
	<title>{t('site_title', 'Dock2Gdansk')} - {t('site_tagline', 'Professional Cargo Transportation')}</title>
</svelte:head>

<!-- Hero Section -->
<section style="background: #0043ce; color: white; padding: 120px 0 64px 0; margin-top: 48px;">
	<div style="max-width: 1200px; margin: 0 auto; padding: 0 16px; text-align: center;">
		
		<h1 style="font-size: 48px; font-weight: normal; margin-bottom: 16px; line-height: 1.2;">
			{heroTitle}
		</h1>
		<p style="font-size: 20px; margin-bottom: 32px; max-width: 800px; margin-left: auto; margin-right: auto;">
			{heroSubtitle}
		</p>
		
	</div>
</section>

<!-- Form Section -->
<section id="inquiry-form" class="form-section">
	<div class="form-wrapper">
		<div class="form-container">
					<h2 style="font-size: 32px; font-weight: bold; margin-bottom: 8px; text-align: center;">
						{formSchema ? getLocalizedText(formSchema.title, 'Submit Your Inquiry') : t('form.title', 'Submit Your Inquiry')}
					</h2>
					<p style="color: #666; margin-bottom: 32px; text-align: center;">
						{formSchema ? getLocalizedText(formSchema.description, 'Fill out the form below') : t('form.description', 'Fill out the form below')}
					</p>

					{#if submitMessage}
						<div class="mb-6">
							<InlineNotification 
								kind={submitStatus}
								title={submitMessage}
								hideCloseButton
							/>
						</div>
					{/if}

					<form on:submit|preventDefault={handleSubmit} class="space-y-6">
						<Grid condensed>
							{#if formSchema?.fields}
								{#each formSchema.fields as field, index}
									<!-- Add Select All checkbox after inquiry_content and before consent checkboxes -->
									{#if field.id === 'privacy_consent' && formSchema.fields.some(f => consentCheckboxIds.includes(f.id))}
										<Column sm={4} md={8} lg={16}>
											<div style="margin-bottom: 24px; padding: 16px; background-color: #f0f8ff; border: 2px dashed #0066cc; border-radius: 8px;">
												<Checkbox
													labelText={$currentLanguage === 'zh' ? '选择所有必需的同意条款' : 'Select all required consents'}
													bind:checked={selectAllConsent}
													on:change={handleSelectAllConsent}
												/>
												<p style="margin: 8px 0 0 0; font-size: 12px; color: #666; font-style: italic;">
													{$currentLanguage === 'zh' ? '选中此框可一次性选择所有同意条款复选框' : 'Check this box to select all consent checkboxes at once'}
												</p>
											</div>
										</Column>
									{/if}
									
									<Column sm={4} md={8} lg={16}>
										<div style="margin-bottom: 24px;">
											{#if field.type === 'text' || field.type === 'email' || field.type === 'tel'}
												<TextInput
													type={field.type}
													labelText={(getLocalizedText(field.label, field.id)) + (field.required ? ' *' : '')}
													placeholder={field.placeholder ? getLocalizedText(field.placeholder, '') : ''}
													bind:value={formData[field.id]}
													required={field.required}
												/>
											{:else if field.type === 'textarea'}
												<TextArea
													labelText={(getLocalizedText(field.label, field.id)) + (field.required ? ' *' : '')}
													placeholder={field.placeholder ? getLocalizedText(field.placeholder, '') : ''}
													bind:value={formData[field.id]}
													rows={field.rows || 4}
													required={field.required}
												/>
											{:else if field.type === 'select'}
												<Select
													labelText={(getLocalizedText(field.label, field.id)) + (field.required ? ' *' : '')}
													placeholder={field.placeholder ? getLocalizedText(field.placeholder, '') : ''}
													bind:selected={formData[field.id]}
													required={field.required}
												>
													{#if field.id === 'cargo_type'}
														<!-- Add placeholder option for cargo type -->
														<SelectItem value="" text={$currentLanguage === 'zh' ? '请选择货物类型' : 'Please select cargo type'} disabled />
														{#each $cargoTypes as cargoType}
															<SelectItem value={cargoType.id} text={cargoType.name} />
														{/each}
													{:else if field.id === 'referral_source'}
														<!-- Add placeholder option for referral source -->
														<SelectItem value="" text={$currentLanguage === 'zh' ? '请选择' : 'Please select'} disabled />
														{#each field.options as option}
															<SelectItem value={option.value} text={getLocalizedText(option.label, option.value)} />
														{/each}
													{:else if field.options}
														{#each field.options as option}
															<SelectItem value={option.value} text={getLocalizedText(option.label, option.value)} />
														{/each}
													{/if}
												</Select>
											{:else if field.type === 'checkbox'}
												<Checkbox
													labelText={(field.description ? getLocalizedText(field.description, field.id) : getLocalizedText(field.label, field.id)) + (field.required ? ' *' : '')}
													bind:checked={formData[field.id]}
													required={field.required}
												/>
											{/if}
										</div>
									</Column>
								{/each}
							{/if}

							<Column sm={4} md={8} lg={16}>
								<div style="margin-top: 24px;">
									<Button 
										type="submit" 
										size="lg" 
										disabled={isSubmitting}
									>
										{#if isSubmitting}
											<Loading withOverlay={false} small />
											{t('form.submitting', 'Submitting...')}
										{:else}
											{formSchema?.submitButton ? getLocalizedText(formSchema.submitButton, 'Submit Inquiry') : t('form.submit', 'Submit Inquiry')}
										{/if}
									</Button>
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
		box-shadow: 0 2px 8px rgba(0,0,0,0.1);
		padding: 48px;
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
		

	}

	/* Tablet adjustments */
	@media (max-width: 1024px) and (min-width: 769px) {
		.form-container {
			padding: 36px 24px;
		}
	}
</style>


