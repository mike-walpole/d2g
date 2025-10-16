<script>
	import {
		Button,
		Tile,
		Grid,
		Column,
		DataTable,
		Toolbar,
		ToolbarContent,
		Breadcrumb,
		BreadcrumbItem,
		Tag,
		ProgressBar,
		ClickableTile,
		Modal,
		TextInput,
		TextArea,
		Select,
		SelectItem,
		Checkbox
	} from 'carbon-components-svelte';
	// Removed carbon icons to avoid import issues
	import { t } from '$lib/stores/config.js';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	let isLoggedIn = false;
	let adminEmail = '';
	let dashboardData = {
		totalSubmissions: 0,
		totalSchemas: 0,
		totalUsers: 0,
		recentSubmissions: []
	};

	// Modal states
	let showManageFormModal = false;
	let showManageCargoModal = false;
	let showManageTeamModal = false;
	let showManageEmailsModal = false;
	let showManageSourcesModal = false;

	// Form data for modals
	let newCargoType = {
		id: '',
		nameEn: '',
		nameZh: '',
		description: ''
	};
	let editingCargoType = null; // For editing existing cargo types
	let newTeamMember = { email: '', role: 'admin' };

	// Sources management data
	let referralSources = [];
	let newSource = {
		id: '',
		nameEn: '',
		nameZh: '',
		description: ''
	};
	let editingSource = null; // For editing existing sources
	let isLoadingSources = false;
	let selectedSchema = null;

	// Team management data
	let teamMembers = [];
	let isLoadingTeam = false;
	let newUserCredentials = null; // Store credentials for newly created user
	let showCredentials = false; // Show credentials modal

	// Email management data
	let clientEmails = [];
	let newEmail = '';
	let isLoadingEmails = false;

	// Form schema management
	let editingSchema = null;
	let editingFields = [];
	let newField = {
		id: '',
		type: 'text',
		labelEn: '',
		labelZh: '',
		placeholderEn: '',
		placeholderZh: '',
		required: false,
		descriptionEn: '',
		descriptionZh: ''
	};

	// Field type options
	const fieldTypes = [
		{ value: 'text', label: 'Text Input' },
		{ value: 'email', label: 'Email Input' },
		{ value: 'tel', label: 'Phone Number' },
		{ value: 'textarea', label: 'Text Area' },
		{ value: 'select', label: 'Dropdown Select' },
		{ value: 'checkbox', label: 'Checkbox' },
		{ value: 'radio', label: 'Radio Buttons' },
		{ value: 'number', label: 'Number Input' },
		{ value: 'date', label: 'Date Picker' }
	];

	// Real data from API
	let cargoTypes = [];
	let formSchema = null;
	let isLoading = false;

	onMount(() => {
		const token = localStorage.getItem('admin-token');
		const email = localStorage.getItem('admin-email');

		if (!token) {
			goto('/kapitanat');
			return;
		}

		isLoggedIn = true;
		adminEmail = email || 'admin@dock2gdansk.com';

		// Load all data
		loadDashboardData();
		loadCargoTypes();
		loadFormSchema();
		loadTeamMembers();
		loadClientEmails();
		loadReferralSources();
	});

	async function loadDashboardData() {
		try {
			console.log('🔄 Fetching submissions from API...');
			const response = await fetch(
				'https://g753am6ace.execute-api.ap-east-1.amazonaws.com/kapitanat/submissions',
				{
					headers: {
						Authorization: `Bearer ${localStorage.getItem('admin-token')}`
					}
				}
			);

			console.log('📡 Submissions API Response:', response.status, response.statusText);

			if (response.ok) {
				const data = await response.json();
				console.log('📊 Submissions Data:', data);

				if (data.success && data.submissions) {
					// Map the API response to the expected format
					const mappedSubmissions = data.submissions.map((submission) => ({
						id: submission.id,
						company: submission.formData?.company || 'N/A',
						email: submission.formData?.email || 'N/A',
						phone:
							submission.formData?.phone_prefix && submission.formData?.phone
								? `${submission.formData.phone_prefix === 'custom' ? submission.formData.custom_phone_prefix || submission.formData.phone_prefix : submission.formData.phone_prefix} ${submission.formData.phone}`
								: 'N/A',
						cargoType: submission.formData?.cargo_type || 'unknown',
						hearAboutUs:
							submission.formData?.hear_about_us || submission.formData?.referral_source || 'N/A',
						inquiryContent: submission.formData?.inquiry_content || 'N/A',
						timestamp: submission.timestamp
					}));

					dashboardData = {
						totalSubmissions: data.count || data.submissions.length,
						totalSchemas: 3,
						totalUsers: 8,
						recentSubmissions: mappedSubmissions
							.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp)) // Sort latest first
							.slice(0, 5) // Show last 5
					};
					console.log('✅ Successfully loaded submissions:', dashboardData.totalSubmissions);
					return;
				} else {
					console.warn('⚠️ API returned unsuccessful response:', data);
				}
			} else {
				console.error('❌ API request failed:', response.status, response.statusText);
			}
		} catch (error) {
			console.error('💥 Error fetching submissions:', error);
		}

		// No fallback - show empty state
		dashboardData = {
			totalSubmissions: 0,
			totalSchemas: 0,
			totalUsers: 0,
			recentSubmissions: []
		};
		console.log('📭 No submissions data available');
	}

	function handleLogout() {
		localStorage.removeItem('admin-token');
		localStorage.removeItem('admin-email');
		goto('/kapitanat');
	}

	// Recent submissions table headers
	const headers = [
		{ key: 'id', value: 'ID' },
		{ key: 'company', value: 'Company' },
		{ key: 'email', value: 'Email' },
		{ key: 'phone', value: 'Phone' },
		{ key: 'cargoType', value: 'Cargo Type' },
		{ key: 'hearAboutUs', value: 'Where did you hear about us' },
		{ key: 'inquiryContent', value: 'Inquiry' },
		{ key: 'timestamp', value: 'Submitted' }
	];

	// Format timestamp
	function formatDate(timestamp) {
		return new Date(timestamp).toLocaleDateString('en-US', {
			year: 'numeric',
			month: 'short',
			day: 'numeric'
		});
	}

	// Helper function to get cargo type display with both ID and name
	function getCargoTypeDisplay(submission) {
		const cargoTypeId = submission.formData?.cargo_type || submission.cargoType;
		const cargoTypeName = submission.cargoTypeName;

		if (!cargoTypeId) return 'Unknown';

		// If we have both ID and resolved name from backend, use them
		if (cargoTypeName && cargoTypeName !== 'Unknown') {
			return `${cargoTypeName} (ID: ${cargoTypeId})`;
		}

		// Fallback: try to find in local cargo types data
		if (cargoTypes && cargoTypes.length > 0) {
			const cargoType = cargoTypes.find((ct) => ct.id === cargoTypeId || ct.value === cargoTypeId);

			if (cargoType) {
				const name = cargoType.name?.en || cargoType.name || cargoType.label || 'Unknown';
				return `${name} (ID: ${cargoTypeId})`;
			}
		}

		// Final fallback: just show the ID
		return `Cargo Type ID: ${cargoTypeId}`;
	}

	// Reactive computed property for enhanced submissions with cargo type names
	$: enhancedSubmissions = dashboardData.recentSubmissions.map((submission) => ({
		...submission,
		cargoType: getCargoTypeDisplay(submission),
		inquiryContent:
			submission.inquiryContent && submission.inquiryContent.length > 50
				? submission.inquiryContent.substring(0, 50) + '...'
				: submission.inquiryContent || 'N/A',
		timestamp: formatDate(submission.timestamp)
	}));

	// Load real cargo types
	async function loadCargoTypes() {
		try {
			console.log('🔄 Fetching cargo types from API...');
			const response = await fetch(
				'https://g753am6ace.execute-api.ap-east-1.amazonaws.com/kapitanat/cargo-types',
				{
					headers: {
						Authorization: `Bearer ${localStorage.getItem('admin-token')}`
					}
				}
			);

			console.log('📡 Cargo Types API Response:', response.status, response.statusText);

			if (response.ok) {
				const data = await response.json();
				console.log('🚢 Cargo Types Data:', data);

				if (data.success && data.cargoTypes) {
					cargoTypes = data.cargoTypes;
					console.log('✅ Successfully loaded cargo types:', cargoTypes.length);
					console.log('📋 Cargo types data structure:', JSON.stringify(cargoTypes, null, 2));
				} else {
					console.warn('⚠️ Cargo types API returned unsuccessful response:', data);
					cargoTypes = [];
				}
			} else {
				console.error('❌ Cargo types API request failed:', response.status, response.statusText);
				cargoTypes = [];
			}
		} catch (error) {
			console.error('💥 Error fetching cargo types:', error);
			cargoTypes = [];
		}
	}

	// Load form schema
	async function loadFormSchema() {
		try {
			console.log('🔄 Fetching form schema from API...');
			const response = await fetch(
				'https://g753am6ace.execute-api.ap-east-1.amazonaws.com/schema?formId=dock2gdansk-main'
			);

			console.log('📡 Form Schema API Response:', response.status, response.statusText);

			if (response.ok) {
				const data = await response.json();
				console.log('📋 Form Schema Data:', data);

				if (data.success && data.schema) {
					formSchema = data.schema;
					console.log(
						'✅ Successfully loaded form schema with',
						formSchema.fields?.length || 0,
						'fields'
					);
				} else {
					console.error('❌ Form schema API returned unsuccessful response:', data);
					formSchema = null;
				}
			} else {
				console.error('❌ Form schema API request failed:', response.status, response.statusText);
				formSchema = null;
			}
		} catch (error) {
			console.error('💥 Error fetching form schema:', error);
			formSchema = null;
		}
	}

	// Modal functions
	async function addCargoType() {
		if (!newCargoType.id.trim() || !newCargoType.nameEn.trim() || !newCargoType.nameZh.trim()) {
			console.error('❌ ID and both English and Chinese names are required');
			return;
		}

		isLoading = true;
		try {
			console.log('🔄 Adding cargo type via API:', newCargoType);

			const response = await fetch(
				'https://g753am6ace.execute-api.ap-east-1.amazonaws.com/kapitanat/cargo-types',
				{
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
						Authorization: `Bearer ${localStorage.getItem('admin-token')}`
					},
					body: JSON.stringify({
						id: newCargoType.id,
						name: {
							en: newCargoType.nameEn,
							zh: newCargoType.nameZh
						},
						description: newCargoType.description
					})
				}
			);

			if (response.ok) {
				const result = await response.json();
				console.log('✅ Cargo type added successfully:', result);

				// Reload cargo types from API
				await loadCargoTypes();

				// Also refresh the config data so frontend gets updated cargo types
				import('$lib/stores/config.js').then((module) => {
					module.loadConfig('en');
				});

				// Reset form
				newCargoType = { id: '', nameEn: '', nameZh: '', description: '' };
				showManageCargoModal = false;
			} else {
				console.error('❌ Failed to add cargo type:', response.status, response.statusText);
			}
		} catch (error) {
			console.error('💥 Error adding cargo type:', error);
		} finally {
			isLoading = false;
		}
	}

	function startEditingCargoType(cargoType) {
		editingCargoType = {
			originalId: cargoType.id || cargoType.value, // Store original ID for backend reference
			id: cargoType.id || cargoType.value,
			nameEn: cargoType.name?.en || cargoType.name || cargoType.label || '',
			nameZh: cargoType.name?.zh || '',
			description: cargoType.description || ''
		};
	}

	function cancelEditingCargoType() {
		editingCargoType = null;
	}

	async function saveEditedCargoType() {
		if (
			!editingCargoType ||
			!editingCargoType.id.trim() ||
			!editingCargoType.nameEn.trim() ||
			!editingCargoType.nameZh.trim()
		) {
			console.error('❌ ID and both English and Chinese names are required');
			return;
		}

		isLoading = true;
		try {
			console.log('🔄 Updating cargo type via API:', editingCargoType);

			const response = await fetch(
				'https://g753am6ace.execute-api.ap-east-1.amazonaws.com/kapitanat/cargo-types',
				{
					method: 'PUT',
					headers: {
						'Content-Type': 'application/json',
						Authorization: `Bearer ${localStorage.getItem('admin-token')}`
					},
					body: JSON.stringify({
						originalId: editingCargoType.originalId,
						id: editingCargoType.id,
						name: {
							en: editingCargoType.nameEn,
							zh: editingCargoType.nameZh
						},
						description: editingCargoType.description
					})
				}
			);

			if (response.ok) {
				const result = await response.json();
				console.log('✅ Cargo type updated successfully:', result);

				// Reload cargo types from API
				await loadCargoTypes();

				// Also refresh the config data so frontend gets updated cargo types
				import('$lib/stores/config.js').then((module) => {
					module.loadConfig('en');
				});

				// Clear editing state
				editingCargoType = null;
			} else {
				console.error('❌ Failed to update cargo type:', response.status, response.statusText);
			}
		} catch (error) {
			console.error('💥 Error updating cargo type:', error);
		} finally {
			isLoading = false;
		}
	}

	async function deleteCargoType(cargoId) {
		isLoading = true;
		try {
			console.log('🔄 Deleting cargo type via API:', cargoId);

			const response = await fetch(
				`https://g753am6ace.execute-api.ap-east-1.amazonaws.com/kapitanat/cargo-types`,
				{
					method: 'DELETE',
					headers: {
						'Content-Type': 'application/json',
						Authorization: `Bearer ${localStorage.getItem('admin-token')}`
					},
					body: JSON.stringify({
						id: cargoId
					})
				}
			);

			if (response.ok) {
				const result = await response.json();
				console.log('✅ Cargo type deleted successfully:', result);

				// Reload cargo types from API
				await loadCargoTypes();

				// Also refresh the config data so frontend gets updated cargo types
				import('$lib/stores/config.js').then((module) => {
					module.loadConfig('en');
				});
			} else {
				console.error('❌ Failed to delete cargo type:', response.status, response.statusText);
			}
		} catch (error) {
			console.error('💥 Error deleting cargo type:', error);
		} finally {
			isLoading = false;
		}
	}

	// Team management functions
	async function loadTeamMembers() {
		isLoadingTeam = true;
		try {
			console.log('🔄 Loading team members from AWS Cognito...');
			const response = await fetch(
				'https://g753am6ace.execute-api.ap-east-1.amazonaws.com/kapitanat/team-members',
				{
					headers: {
						Authorization: `Bearer ${localStorage.getItem('admin-token')}`
					}
				}
			);

			console.log('📡 Team API Response:', response.status, response.statusText);

			if (response.ok) {
				const data = await response.json();
				console.log('👥 Team Members Data:', data);

				if (data.success && data.users) {
					teamMembers = data.users;
					console.log('✅ Successfully loaded team members:', teamMembers.length);
				} else {
					console.warn('⚠️ Team API returned unsuccessful response:', data);
					teamMembers = [];
				}
			} else {
				console.error('❌ Team API request failed:', response.status, response.statusText);
				teamMembers = [];
			}
		} catch (error) {
			console.error('💥 Error fetching team members:', error);
			teamMembers = [];
		} finally {
			isLoadingTeam = false;
		}
	}

	async function addTeamMember() {
		if (!newTeamMember.email.trim()) {
			console.error('❌ Email is required');
			return;
		}

		// Basic email validation
		const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
		if (!emailRegex.test(newTeamMember.email)) {
			console.error('❌ Invalid email format');
			return;
		}

		isLoadingTeam = true;
		try {
			console.log('🔄 Adding team member via AWS Cognito API:', newTeamMember);

			const response = await fetch(
				'https://g753am6ace.execute-api.ap-east-1.amazonaws.com/kapitanat/team-members',
				{
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
						Authorization: `Bearer ${localStorage.getItem('admin-token')}`
					},
					body: JSON.stringify({
						email: newTeamMember.email,
						isAdmin: newTeamMember.role === 'admin',
						temporaryPassword: 'TempPass123!'
					})
				}
			);

			if (response.ok) {
				const result = await response.json();
				console.log('✅ Team member added successfully:', result);

				// Store credentials for display
				newUserCredentials = {
					email: newTeamMember.email,
					temporaryPassword: result.temporaryPassword || 'TempPass123!',
					loginUrl: 'https://www.dock2gdansk.com/kapitanat'
				};
				showCredentials = true;

				// Reload team members from API
				await loadTeamMembers();

				// Reset form
				newTeamMember = { email: '', role: 'admin' };
				showManageTeamModal = false;
			} else {
				const errorData = await response.json();
				console.error(
					'❌ Failed to add team member:',
					response.status,
					response.statusText,
					errorData
				);
			}
		} catch (error) {
			console.error('💥 Error adding team member:', error);
		} finally {
			isLoadingTeam = false;
		}
	}

	async function removeTeamMember(userEmail) {
		if (!userEmail) return;

		// Prevent removing self
		if (userEmail === adminEmail) {
			console.warn('⚠️ Cannot remove yourself from the team');
			return;
		}

		isLoadingTeam = true;
		try {
			console.log('🔄 Removing team member via AWS Cognito API:', userEmail);

			const response = await fetch(
				`https://g753am6ace.execute-api.ap-east-1.amazonaws.com/kapitanat/team-members?username=${encodeURIComponent(userEmail)}`,
				{
					method: 'DELETE',
					headers: {
						Authorization: `Bearer ${localStorage.getItem('admin-token')}`
					}
				}
			);

			if (response.ok) {
				const result = await response.json();
				console.log('✅ Team member removed successfully:', result);

				// Reload team members from API
				await loadTeamMembers();
			} else {
				const errorData = await response.json();
				console.error(
					'❌ Failed to remove team member:',
					response.status,
					response.statusText,
					errorData
				);
			}
		} catch (error) {
			console.error('💥 Error removing team member:', error);
		} finally {
			isLoadingTeam = false;
		}
	}

	async function updateTeamMemberRole(userEmail, newRole) {
		if (!userEmail || !newRole) return;

		isLoadingTeam = true;
		try {
			console.log('🔄 Updating team member role via AWS Cognito API:', userEmail, newRole);

			const response = await fetch(
				'https://g753am6ace.execute-api.ap-east-1.amazonaws.com/kapitanat/team-members',
				{
					method: 'PUT',
					headers: {
						'Content-Type': 'application/json',
						Authorization: `Bearer ${localStorage.getItem('admin-token')}`
					},
					body: JSON.stringify({
						email: userEmail,
						role: newRole
					})
				}
			);

			if (response.ok) {
				const result = await response.json();
				console.log('✅ Team member role updated successfully:', result);

				// Reload team members from API
				await loadTeamMembers();
			} else {
				const errorData = await response.json();
				console.error(
					'❌ Failed to update team member role:',
					response.status,
					response.statusText,
					errorData
				);
			}
		} catch (error) {
			console.error('💥 Error updating team member role:', error);
		} finally {
			isLoadingTeam = false;
		}
	}

	// Form schema management functions
	async function openManageFormModal() {
		console.log('🔄 Opening manage form modal...');

		// Always fetch fresh data from DynamoDB - no caching
		try {
			console.log('📡 Fetching latest schema from DynamoDB...');
			const response = await fetch(
				'https://g753am6ace.execute-api.ap-east-1.amazonaws.com/schema?formId=dock2gdansk-main'
			);

			if (response.ok) {
				const data = await response.json();
				console.log('📋 Fresh schema from DynamoDB:', data);

				if (data.success && data.schema && data.schema.fields) {
					// Update the cached formSchema with fresh data
					formSchema = data.schema;

					// Set editing data from fresh schema
					editingSchema = JSON.parse(JSON.stringify(data.schema)); // Deep copy
					editingFields = [...(data.schema.fields || [])];
					console.log('✅ Set editingSchema from fresh data:', editingSchema);
					console.log('✅ Set editingFields from fresh data:', editingFields);
				} else {
					console.error('❌ Fresh schema API returned unsuccessful response:', data);
					editingSchema = null;
					editingFields = [];
				}
			} else {
				console.error('❌ Fresh schema API request failed:', response.status, response.statusText);
				editingSchema = null;
				editingFields = [];
			}
		} catch (error) {
			console.error('💥 Error fetching fresh schema:', error);
			editingSchema = null;
			editingFields = [];
		}

		showManageFormModal = true;
	}

	function addNewField() {
		if (!newField.id.trim() || !newField.labelEn.trim() || !newField.labelZh.trim()) {
			console.warn('Field ID and both language labels are required');
			return;
		}

		// Check if field ID already exists
		if (editingFields.some((f) => f.id === newField.id)) {
			console.warn('Field ID already exists');
			return;
		}

		const field = {
			id: newField.id,
			type: newField.type,
			label: {
				en: newField.labelEn,
				zh: newField.labelZh
			},
			required: newField.required
		};

		// Add placeholder if provided
		if (newField.placeholderEn || newField.placeholderZh) {
			field.placeholder = {
				en: newField.placeholderEn,
				zh: newField.placeholderZh
			};
		}

		// Add description if provided
		if (newField.descriptionEn || newField.descriptionZh) {
			field.description = {
				en: newField.descriptionEn,
				zh: newField.descriptionZh
			};
		}

		// Add validation for certain field types
		if (newField.type === 'text' || newField.type === 'email') {
			field.validation = {
				maxLength: 100,
				minLength: 2
			};
		}

		editingFields.push(field);

		// Reset new field form
		newField = {
			id: '',
			type: 'text',
			labelEn: '',
			labelZh: '',
			placeholderEn: '',
			placeholderZh: '',
			required: false,
			descriptionEn: '',
			descriptionZh: ''
		};
	}

	function deleteField(fieldId) {
		editingFields = editingFields.filter((f) => f.id !== fieldId);
	}

	function updateField(fieldId, property, value) {
		const field = editingFields.find((f) => f.id === fieldId);
		if (field) {
			if (property.includes('.')) {
				const [obj, key] = property.split('.');
				if (!field[obj]) field[obj] = {};
				field[obj][key] = value;
			} else {
				field[property] = value;
			}
		}
	}

	async function saveFormSchema() {
		if (!editingSchema || editingFields.length === 0) return;

		isLoading = true;
		try {
			// Create new version of the schema
			const newSchema = {
				...editingSchema,
				fields: editingFields,
				version: generateNewVersion(editingSchema.version || '1.0.0'),
				updatedAt: new Date().toISOString()
			};

			console.log('Saving new schema version:', newSchema.version);

			// Make API call to save new schema version
			const response = await fetch(
				'https://g753am6ace.execute-api.ap-east-1.amazonaws.com/kapitanat/schemas',
				{
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
						Authorization: `Bearer ${localStorage.getItem('admin-token')}`
					},
					body: JSON.stringify({
						formId: 'dock2gdansk-main',
						description: `Schema updated via admin dashboard - ${new Date().toLocaleString()}`,
						schema: {
							title: newSchema.title,
							description: newSchema.description,
							fields: newSchema.fields,
							submitButton: newSchema.submitButton,
							settings: newSchema.settings
						}
					})
				}
			);

			if (response.ok) {
				const result = await response.json();
				console.log('✅ Schema saved successfully:', result);

				// No need to reload - next time modal opens it will fetch fresh data
				showManageFormModal = false;
			} else {
				console.error('❌ Failed to save schema:', response.status, response.statusText);
				// Keep modal open to show error
			}
		} catch (error) {
			console.error('💥 Error saving schema:', error);
			// Keep modal open to show error
		} finally {
			isLoading = false;
		}
	}

	function generateNewVersion(currentVersion) {
		const parts = currentVersion.split('.');
		const major = parseInt(parts[0]);
		const minor = parseInt(parts[1]);
		const patch = parseInt(parts[2]) || 0;
		return `${major}.${minor}.${patch + 1}`;
	}

	// Email management functions
	async function loadClientEmails() {
		isLoadingEmails = true;
		try {
			console.log('🔄 Loading client emails from API...');
			const response = await fetch(
				'https://g753am6ace.execute-api.ap-east-1.amazonaws.com/kapitanat/emails',
				{
					headers: {
						Authorization: `Bearer ${localStorage.getItem('admin-token')}`
					}
				}
			);

			console.log('📡 Client Emails API Response:', response.status, response.statusText);

			if (response.ok) {
				const data = await response.json();
				console.log('📧 Client Emails Data:', data);

				if (data.success && data.emails) {
					clientEmails = data.emails;
					console.log('✅ Successfully loaded client emails:', clientEmails.length);
				} else {
					console.warn('⚠️ Client emails API returned unsuccessful response:', data);
					// Initialize with default emails if none exist
					clientEmails = [
						{
							id: '1',
							email: 'Marek.Machalski@portgdansk.pl',
							name: 'Marek Machalski',
							addedAt: new Date().toISOString(),
							active: true
						},
						{
							id: '2',
							email: 'michal@dagodigital.com',
							name: 'Michal',
							addedAt: new Date().toISOString(),
							active: true
						}
					];
				}
			} else {
				console.error('❌ Client emails API request failed:', response.status, response.statusText);
				// Initialize with default emails on API failure
				clientEmails = [
					{
						id: '1',
						email: 'Marek.Machalski@portgdansk.pl',
						name: 'Marek Machalski',
						addedAt: new Date().toISOString(),
						active: true
					},
					{
						id: '2',
						email: 'michal@dagodigital.com',
						name: 'Michal',
						addedAt: new Date().toISOString(),
						active: true
					}
				];
			}
		} catch (error) {
			console.error('💥 Error fetching client emails:', error);
			// Initialize with default emails on error
			clientEmails = [
				{
					id: '1',
					email: 'Marek.Machalski@portgdansk.pl',
					name: 'Marek Machalski',
					addedAt: new Date().toISOString(),
					active: true
				},
				{
					id: '2',
					email: 'michal@dagodigital.com',
					name: 'Michal',
					addedAt: new Date().toISOString(),
					active: true
				}
			];
		} finally {
			isLoadingEmails = false;
		}
	}

	async function addClientEmail() {
		if (!newEmail.trim()) {
			console.error('❌ Email is required');
			return;
		}

		// Basic email validation
		const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
		if (!emailRegex.test(newEmail)) {
			console.error('❌ Invalid email format');
			return;
		}

		// Check if email already exists
		if (clientEmails.some((e) => e.email.toLowerCase() === newEmail.toLowerCase())) {
			console.error('❌ Email already exists');
			return;
		}

		isLoadingEmails = true;
		try {
			console.log('🔄 Adding client email via API:', newEmail);

			const response = await fetch(
				'https://g753am6ace.execute-api.ap-east-1.amazonaws.com/kapitanat/emails',
				{
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
						Authorization: `Bearer ${localStorage.getItem('admin-token')}`
					},
					body: JSON.stringify({
						email: newEmail.trim(),
						name: newEmail.split('@')[0], // Extract name from email
						active: true
					})
				}
			);

			if (response.ok) {
				const result = await response.json();
				console.log('✅ Client email added successfully:', result);

				// Reload client emails from API
				await loadClientEmails();

				// Reset form
				newEmail = '';
				showManageEmailsModal = false;
			} else {
				const errorData = await response.json();
				console.error(
					'❌ Failed to add client email:',
					response.status,
					response.statusText,
					errorData
				);

				// Fallback: add locally if API fails
				const newEmailObj = {
					id: Date.now().toString(),
					email: newEmail.trim(),
					name: newEmail.split('@')[0],
					addedAt: new Date().toISOString(),
					active: true
				};
				clientEmails = [...clientEmails, newEmailObj];
				newEmail = '';
				showManageEmailsModal = false;
			}
		} catch (error) {
			console.error('💥 Error adding client email:', error);

			// Fallback: add locally if API fails
			const newEmailObj = {
				id: Date.now().toString(),
				email: newEmail.trim(),
				name: newEmail.split('@')[0],
				addedAt: new Date().toISOString(),
				active: true
			};
			clientEmails = [...clientEmails, newEmailObj];
			newEmail = '';
			showManageEmailsModal = false;
		} finally {
			isLoadingEmails = false;
		}
	}

	async function removeClientEmail(emailObj) {
		if (!emailObj) return;

		// Support both old (emailId string) and new (email object) signatures
		const emailId = typeof emailObj === 'string' ? emailObj : emailObj.id;
		const emailAddress = typeof emailObj === 'object' ? emailObj.email : null;

		if (!emailId && !emailAddress) return;

		isLoadingEmails = true;
		try {
			console.log('🔄 Removing client email via API:', emailObj);

			const requestBody = {};
			if (emailId) {
				requestBody.id = emailId;
			} else if (emailAddress) {
				requestBody.email = emailAddress;
			}

			const response = await fetch(
				'https://g753am6ace.execute-api.ap-east-1.amazonaws.com/kapitanat/emails',
				{
					method: 'DELETE',
					headers: {
						'Content-Type': 'application/json',
						Authorization: `Bearer ${localStorage.getItem('admin-token')}`
					},
					body: JSON.stringify(requestBody)
				}
			);

			if (response.ok) {
				const result = await response.json();
				console.log('✅ Client email removed successfully:', result);

				// Reload client emails from API
				await loadClientEmails();
			} else {
				const errorData = await response.json();
				console.error(
					'❌ Failed to remove client email:',
					response.status,
					response.statusText,
					errorData
				);

				// Fallback: remove locally if API fails
				if (emailId) {
					clientEmails = clientEmails.filter((e) => e.id !== emailId);
				} else {
					clientEmails = clientEmails.filter((e) => e.email !== emailAddress);
				}
			}
		} catch (error) {
			console.error('💥 Error removing client email:', error);

			// Fallback: remove locally if API fails
			if (emailId) {
				clientEmails = clientEmails.filter((e) => e.id !== emailId);
			} else {
				clientEmails = clientEmails.filter((e) => e.email !== emailAddress);
			}
		} finally {
			isLoadingEmails = false;
		}
	}

	async function toggleEmailStatus(emailId, newStatus) {
		if (!emailId) return;

		isLoadingEmails = true;
		try {
			console.log('🔄 Updating client email status via API:', emailId, newStatus);

			const response = await fetch(
				'https://g753am6ace.execute-api.ap-east-1.amazonaws.com/kapitanat/emails',
				{
					method: 'PUT',
					headers: {
						'Content-Type': 'application/json',
						Authorization: `Bearer ${localStorage.getItem('admin-token')}`
					},
					body: JSON.stringify({
						id: emailId,
						active: newStatus
					})
				}
			);

			if (response.ok) {
				const result = await response.json();
				console.log('✅ Client email status updated successfully:', result);

				// Reload client emails from API
				await loadClientEmails();
			} else {
				const errorData = await response.json();
				console.error(
					'❌ Failed to update client email status:',
					response.status,
					response.statusText,
					errorData
				);

				// Fallback: update locally if API fails
				clientEmails = clientEmails.map((e) =>
					e.id === emailId ? { ...e, active: newStatus } : e
				);
			}
		} catch (error) {
			console.error('💥 Error updating client email status:', error);

			// Fallback: update locally if API fails
			clientEmails = clientEmails.map((e) => (e.id === emailId ? { ...e, active: newStatus } : e));
		} finally {
			isLoadingEmails = false;
		}
	}

	// Referral Sources management functions
	async function loadReferralSources() {
		isLoadingSources = true;
		try {
			console.log('🔄 Loading referral sources from API...');
			const response = await fetch(
				'https://g753am6ace.execute-api.ap-east-1.amazonaws.com/kapitanat/referral-sources',
				{
					headers: {
						Authorization: `Bearer ${localStorage.getItem('admin-token')}`
					}
				}
			);

			console.log('📡 Referral Sources API Response:', response.status, response.statusText);

			if (response.ok) {
				const data = await response.json();
				console.log('📋 Referral Sources Data:', data);

				if (data.success && data.sources) {
					referralSources = data.sources;
					console.log('✅ Successfully loaded referral sources:', referralSources.length);
				} else {
					console.warn('⚠️ Referral sources API returned unsuccessful response:', data);
					referralSources = [];
				}
			} else {
				console.error(
					'❌ Referral sources API request failed:',
					response.status,
					response.statusText
				);
				referralSources = [];
			}
		} catch (error) {
			console.error('💥 Error fetching referral sources:', error);
			referralSources = [];
		} finally {
			isLoadingSources = false;
		}
	}

	async function addReferralSource() {
		if (!newSource.id.trim() || !newSource.nameEn.trim() || !newSource.nameZh.trim()) {
			console.error('❌ ID and both English and Chinese names are required');
			return;
		}

		isLoadingSources = true;
		try {
			console.log('🔄 Adding referral source via API:', newSource);

			const response = await fetch(
				'https://g753am6ace.execute-api.ap-east-1.amazonaws.com/kapitanat/referral-sources',
				{
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
						Authorization: `Bearer ${localStorage.getItem('admin-token')}`
					},
					body: JSON.stringify({
						id: newSource.id,
						name: {
							en: newSource.nameEn,
							zh: newSource.nameZh
						},
						description: newSource.description
					})
				}
			);

			if (response.ok) {
				const result = await response.json();
				console.log('✅ Referral source added successfully:', result);

				// Reload referral sources from API
				await loadReferralSources();

				// Reset form
				newSource = { id: '', nameEn: '', nameZh: '', description: '' };
				showManageSourcesModal = false;
			} else {
				console.error('❌ Failed to add referral source:', response.status, response.statusText);
			}
		} catch (error) {
			console.error('💥 Error adding referral source:', error);
		} finally {
			isLoadingSources = false;
		}
	}

	function startEditingSource(source) {
		editingSource = {
			originalId: source.id || source.value,
			id: source.id || source.value,
			nameEn: source.name?.en || source.name || source.label || '',
			nameZh: source.name?.zh || '',
			description: source.description || ''
		};
	}

	function cancelEditingSource() {
		editingSource = null;
	}

	async function saveEditedSource() {
		if (
			!editingSource ||
			!editingSource.id.trim() ||
			!editingSource.nameEn.trim() ||
			!editingSource.nameZh.trim()
		) {
			console.error('❌ ID and both English and Chinese names are required');
			return;
		}

		isLoadingSources = true;
		try {
			console.log('🔄 Updating referral source via API:', editingSource);

			const response = await fetch(
				'https://g753am6ace.execute-api.ap-east-1.amazonaws.com/kapitanat/referral-sources',
				{
					method: 'PUT',
					headers: {
						'Content-Type': 'application/json',
						Authorization: `Bearer ${localStorage.getItem('admin-token')}`
					},
					body: JSON.stringify({
						originalId: editingSource.originalId,
						id: editingSource.id,
						name: {
							en: editingSource.nameEn,
							zh: editingSource.nameZh
						},
						description: editingSource.description
					})
				}
			);

			if (response.ok) {
				const result = await response.json();
				console.log('✅ Referral source updated successfully:', result);

				// Reload referral sources from API
				await loadReferralSources();

				// Clear editing state
				editingSource = null;
			} else {
				console.error('❌ Failed to update referral source:', response.status, response.statusText);
			}
		} catch (error) {
			console.error('💥 Error updating referral source:', error);
		} finally {
			isLoadingSources = false;
		}
	}

	async function deleteReferralSource(sourceId) {
		isLoadingSources = true;
		try {
			console.log('🔄 Deleting referral source via API:', sourceId);

			const response = await fetch(
				`https://g753am6ace.execute-api.ap-east-1.amazonaws.com/kapitanat/referral-sources`,
				{
					method: 'DELETE',
					headers: {
						'Content-Type': 'application/json',
						Authorization: `Bearer ${localStorage.getItem('admin-token')}`
					},
					body: JSON.stringify({
						id: sourceId
					})
				}
			);

			if (response.ok) {
				const result = await response.json();
				console.log('✅ Referral source deleted successfully:', result);

				// Reload referral sources from API
				await loadReferralSources();
			} else {
				console.error('❌ Failed to delete referral source:', response.status, response.statusText);
			}
		} catch (error) {
			console.error('💥 Error deleting referral source:', error);
		} finally {
			isLoadingSources = false;
		}
	}

	// Copy credentials to clipboard
	async function copyCredentials() {
		if (!newUserCredentials) return;

		const credentialsText = `New Team Member Login Credentials:

Email: ${newUserCredentials.email}
Temporary Password: ${newUserCredentials.temporaryPassword}
Login URL: ${newUserCredentials.loginUrl}

Please share these credentials securely with the new team member. They will be required to change their password on first login.`;

		try {
			await navigator.clipboard.writeText(credentialsText);
			console.log('✅ Credentials copied to clipboard');
		} catch (err) {
			console.error('❌ Failed to copy credentials:', err);
			// Fallback: select text for manual copy
			const textArea = document.createElement('textarea');
			textArea.value = credentialsText;
			document.body.appendChild(textArea);
			textArea.select();
			document.execCommand('copy');
			document.body.removeChild(textArea);
		}
	}

	// Download Schema function
	async function downloadSchema() {
		try {
			console.log('🔄 Downloading current schema...');

			const response = await fetch(
				`https://g753am6ace.execute-api.ap-east-1.amazonaws.com/kapitanat/download-schema?version=current`,
				{
					method: 'GET',
					headers: {
						Authorization: 'Bearer mock-jwt-token-dev-admin'
					}
				}
			);

			if (response.ok) {
				// Get the filename from Content-Disposition header or create a default
				const contentDisposition = response.headers.get('Content-Disposition');
				let filename = 'd2g-schema-current.json';

				if (contentDisposition) {
					const filenameMatch = contentDisposition.match(/filename="(.+)"/);
					if (filenameMatch) {
						filename = filenameMatch[1];
					}
				}

				// Get the JSON content
				const jsonData = await response.text();

				// Create blob and download
				const blob = new Blob([jsonData], { type: 'application/json' });
				const url = window.URL.createObjectURL(blob);
				const a = document.createElement('a');
				a.href = url;
				a.download = filename;
				document.body.appendChild(a);
				a.click();
				window.URL.revokeObjectURL(url);
				document.body.removeChild(a);

				console.log('✅ Schema downloaded successfully:', filename);
			} else {
				console.error('❌ Failed to download schema:', response.status, response.statusText);
			}
		} catch (error) {
			console.error('❌ Error downloading schema:', error);
		}
	}

	// Download Data function
	async function downloadData() {
		try {
			console.log('🔄 Downloading all submissions data...');

			const response = await fetch(
				'https://g753am6ace.execute-api.ap-east-1.amazonaws.com/kapitanat/submissions',
				{
					headers: {
						Authorization: `Bearer ${localStorage.getItem('admin-token')}`
					}
				}
			);

			if (response.ok) {
				const data = await response.json();
				console.log('📡 Fetched data:', data);

				if (data.success && Array.isArray(data.submissions)) {
					// Map submissions to match dashboard format
					const allSubmissions = data.submissions.map((submission) => ({
						id: submission.id,
						company: submission.formData?.company || 'N/A',
						email: submission.formData?.email || 'N/A',
						phone: submission.formData?.phone || 'N/A',
						cargoType: getCargoTypeDisplay(submission),
						hearAboutUs:
							submission.formData?.hear_about_us || submission.formData?.referral_source || 'N/A',
						inquiryContent: submission.formData?.inquiry_content || 'N/A',
						timestamp: formatDate(submission.timestamp)
					}));

					// Convert to CSV format
					const csvHeaders = [
						'ID',
						'Company',
						'Email',
						'Phone',
						'Cargo Type',
						'Where did you hear about us',
						'Inquiry',
						'Submitted'
					];

					// Escape CSV fields (handle commas, quotes, newlines)
					const escapeCSVField = (field) => {
						if (field === null || field === undefined) return '';
						const stringField = String(field);
						// If field contains comma, quote, or newline, wrap in quotes and escape internal quotes
						if (
							stringField.includes(',') ||
							stringField.includes('"') ||
							stringField.includes('\n')
						) {
							return `"${stringField.replace(/"/g, '""')}"`;
						}
						return stringField;
					};

					const csvRows = [
						csvHeaders.join(','),
						...allSubmissions.map((sub) =>
							[
								escapeCSVField(sub.id),
								escapeCSVField(sub.company),
								escapeCSVField(sub.email),
								escapeCSVField(sub.phone),
								escapeCSVField(sub.cargoType),
								escapeCSVField(sub.hearAboutUs),
								escapeCSVField(sub.inquiryContent),
								escapeCSVField(sub.timestamp)
							].join(',')
						)
					];

					const csvContent = csvRows.join('\n');

					// Create blob and download
					const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
					const url = window.URL.createObjectURL(blob);
					const a = document.createElement('a');
					a.href = url;
					const timestamp = new Date().toISOString().split('T')[0];
					a.download = `d2g-submissions-${timestamp}.csv`;
					document.body.appendChild(a);
					a.click();
					window.URL.revokeObjectURL(url);
					document.body.removeChild(a);

					console.log('✅ Data downloaded successfully:', allSubmissions.length, 'submissions');
				} else {
					console.error('❌ Invalid data format received');
				}
			} else {
				console.error('❌ Failed to download data:', response.status, response.statusText);
			}
		} catch (error) {
			console.error('❌ Error downloading data:', error);
		}
	}
</script>

<svelte:head>
	<title>{t('admin.dashboard', 'Dashboard')} - Dock2Gdansk Admin</title>
</svelte:head>

{#if isLoggedIn}
	<div class="dashboard-container">
		<!-- Header -->
		<div class="header-section">
			<Breadcrumb noTrailingSlash>
				<BreadcrumbItem href="/kapitanat/dashboard">
					{t('admin.dashboard', 'Dashboard')}
				</BreadcrumbItem>
			</Breadcrumb>

			<div class="header-content">
				<div class="header-info">
					<h1 class="dashboard-title">
						{t('admin.dashboard', 'Dashboard')}
					</h1>
					<p class="welcome-text">Welcome back, {adminEmail}</p>
				</div>

				<Button kind="danger-ghost" on:click={handleLogout}>
					🚪 {t('admin.logout', 'Logout')}
				</Button>
			</div>
		</div>

		<!-- Quick Actions and System Status -->
		<div class="dashboard-row">
			<div class="dashboard-column">
				<Tile class="tile-padding">
					<h2 class="section-title">Quick Actions</h2>
					<div class="button-grid">
						<Button kind="primary" on:click={openManageFormModal} class="action-button">
							Manage Form
						</Button>
						<Button
							kind="tertiary"
							on:click={() => {
								showManageCargoModal = true;
								editingCargoType = null;
							}}
							class="action-button"
						>
							Manage Cargo
						</Button>
						<Button
							kind="tertiary"
							on:click={() => (showManageTeamModal = true)}
							class="action-button"
						>
							Manage Team
						</Button>
						<Button
							kind="tertiary"
							on:click={() => (showManageEmailsModal = true)}
							class="action-button"
						>
							Manage Emails
						</Button>
						<Button
							kind="tertiary"
							on:click={() => {
								showManageSourcesModal = true;
								editingSource = null;
							}}
							class="action-button"
						>
							Manage Sources
						</Button>
						<Button kind="tertiary" on:click={downloadSchema} class="action-button">
							Download Schema
						</Button>
						<Button kind="tertiary" on:click={downloadData} class="action-button">
							Download Data
						</Button>
					</div>
				</Tile>
			</div>

			<div class="dashboard-column">
				<Tile class="tile-padding">
					<h2 class="section-title">System Status</h2>
					<div class="status-list">
						<div class="status-item">
							<span class="status-label">API Health</span>
							<div class="status-indicator status-ok">
								<span>✓</span>
							</div>
						</div>
						<div class="status-item">
							<span class="status-label">Database Status</span>
							<div class="status-indicator status-ok">
								<span>✓</span>
							</div>
						</div>
						<div class="status-item">
							<span class="status-label">Email Service</span>
							<div class="status-indicator status-ok">
								<span>✓</span>
							</div>
						</div>
					</div>
				</Tile>
			</div>
		</div>

		<!-- Recent Submissions -->
		<Tile class="submissions-tile">
			<h2 class="section-title">Recent Submissions</h2>

			<DataTable {headers} rows={enhancedSubmissions} />

			{#if dashboardData.recentSubmissions.length === 0}
				<div style="text-align: center; padding: 32px; color: #666;">
					<div style="font-size: 48px; margin-bottom: 16px;">📭</div>
					<h3 style="margin-bottom: 8px;">No submissions found</h3>
					<p style="margin: 0;">
						Either no form submissions exist yet, or there was an error loading data from the
						database.
					</p>
					<p style="margin: 8px 0 0 0; font-size: 14px; color: #999;">
						Check the browser console for API error details.
					</p>
				</div>
			{/if}
		</Tile>

		<!-- Modals -->
		<!-- Manage Form Modal -->
		<Modal
			bind:open={showManageFormModal}
			modalHeading="Manage Form Schema"
			primaryButtonText="Save Changes"
			secondaryButtonText="Cancel"
			on:click:button--secondary={() => {
				showManageFormModal = false;
				editingSchema = null;
				editingFields = [];
			}}
			on:click:button--primary={saveFormSchema}
			size="lg"
		>
			{#if editingSchema}
				<!-- Debug info (remove in production) -->
				<div
					style="margin-bottom: 16px; padding: 8px; background: #f0f0f0; border-radius: 4px; font-size: 12px;"
				>
					<strong>Debug:</strong> Schema loaded with {editingFields.length} fields | Version: {editingSchema.version ||
						'1.0.0'} | API Version: {formSchema?.version || 'unknown'}
				</div>

				<!-- Form Title Section -->
				<div style="margin-bottom: 24px; padding: 16px; background: #f8f9fa; border-radius: 6px;">
					<h4 style="margin: 0 0 12px 0;">Form Title</h4>
					<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
						<TextInput labelText="English Title" bind:value={editingSchema.title.en} />
						<TextInput labelText="Chinese Title" bind:value={editingSchema.title.zh} />
					</div>
				</div>

				<!-- Add New Field Section -->
				<div style="margin-bottom: 24px; padding: 16px; background: #e8f4fd; border-radius: 6px;">
					<h4 style="margin: 0 0 16px 0;">➕ Add New Field</h4>
					<div
						style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 12px;"
					>
						<TextInput
							labelText="Field ID *"
							placeholder="e.g., company_name"
							bind:value={newField.id}
						/>
						<Select labelText="Field Type *" bind:selected={newField.type}>
							{#each fieldTypes as type}
								<SelectItem value={type.value} text={type.label} />
							{/each}
						</Select>
					</div>

					<div
						style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 12px;"
					>
						<TextInput
							labelText="Label (English) *"
							placeholder="e.g., Company Name"
							bind:value={newField.labelEn}
						/>
						<TextInput
							labelText="Label (Chinese) *"
							placeholder="e.g., 公司名称"
							bind:value={newField.labelZh}
						/>
					</div>

					<div
						style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 12px;"
					>
						<TextInput
							labelText="Placeholder (English)"
							placeholder="e.g., Enter your company name"
							bind:value={newField.placeholderEn}
						/>
						<TextInput
							labelText="Placeholder (Chinese)"
							placeholder="e.g., 请输入您的公司名称"
							bind:value={newField.placeholderZh}
						/>
					</div>

					<div
						style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 12px;"
					>
						<TextInput
							labelText="Description (English)"
							placeholder="e.g., Your company's official name"
							bind:value={newField.descriptionEn}
						/>
						<TextInput
							labelText="Description (Chinese)"
							placeholder="e.g., 您公司的正式名称"
							bind:value={newField.descriptionZh}
						/>
					</div>

					<div style="margin-bottom: 12px;">
						<Checkbox labelText="Required Field" bind:checked={newField.required} />
					</div>

					<Button
						kind="tertiary"
						size="sm"
						on:click={addNewField}
						disabled={!newField.id || !newField.labelEn || !newField.labelZh}
					>
						Add Field
					</Button>
				</div>

				<!-- Existing Fields Section -->
				<div style="margin-bottom: 16px;">
					<h4>Current Fields ({editingFields.length})</h4>
					{#if editingFields.length > 0}
						<div
							style="max-height: 400px; overflow-y: auto; border: 1px solid #ddd; border-radius: 6px;"
						>
							{#each editingFields as field, index}
								<div
									style="padding: 16px; border-bottom: 1px solid #eee; {index ===
									editingFields.length - 1
										? 'border-bottom: none;'
										: ''}"
								>
									<!-- Field Header -->
									<div
										style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;"
									>
										<div style="display: flex; align-items: center; gap: 8px;">
											<strong style="color: #333;">#{index + 1}: {field.id}</strong>
											<span
												style="background: #e1f5fe; color: #0277bd; padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight: 500;"
											>
												{field.type}
											</span>
											{#if field.required}
												<span
													style="background: #ffebee; color: #c62828; padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight: 500;"
												>
													Required
												</span>
											{/if}
										</div>
										<Button kind="danger-ghost" size="sm" on:click={() => deleteField(field.id)}>
											🗑️ Delete
										</Button>
									</div>

									<!-- Editable Fields -->
									<div
										style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 8px;"
									>
										<TextInput
											labelText="Label (English)"
											bind:value={field.label.en}
											on:input={(e) => updateField(field.id, 'label.en', e.target.value)}
										/>
										<TextInput
											labelText="Label (Chinese)"
											bind:value={field.label.zh}
											on:input={(e) => updateField(field.id, 'label.zh', e.target.value)}
										/>
									</div>

									{#if field.placeholder}
										<div
											style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 8px;"
										>
											<TextInput
												labelText="Placeholder (English)"
												bind:value={field.placeholder.en}
												on:input={(e) => updateField(field.id, 'placeholder.en', e.target.value)}
											/>
											<TextInput
												labelText="Placeholder (Chinese)"
												bind:value={field.placeholder.zh}
												on:input={(e) => updateField(field.id, 'placeholder.zh', e.target.value)}
											/>
										</div>
									{/if}

									{#if field.description}
										<div
											style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 8px;"
										>
											<TextInput
												labelText="Description (English)"
												bind:value={field.description.en}
												on:input={(e) => updateField(field.id, 'description.en', e.target.value)}
											/>
											<TextInput
												labelText="Description (Chinese)"
												bind:value={field.description.zh}
												on:input={(e) => updateField(field.id, 'description.zh', e.target.value)}
											/>
										</div>
									{/if}

									<div style="margin-top: 8px;">
										<Checkbox
											labelText="Required Field"
											checked={field.required}
											on:change={(e) => updateField(field.id, 'required', e.target.checked)}
										/>
									</div>
								</div>
							{/each}
						</div>
					{:else}
						<div style="text-align: center; padding: 32px; color: #666;">
							<div style="font-size: 24px; margin-bottom: 8px;">📝</div>
							<p style="margin: 0;">No fields defined yet</p>
							<p style="margin: 4px 0 0 0; font-size: 12px; color: #999;">
								Add fields using the form above
							</p>
						</div>
					{/if}
				</div>

				<div
					style="margin-top: 16px; padding: 12px; background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 4px;"
				>
					<p style="margin: 0; font-size: 14px; color: #856404;">
						<strong>💡 Note:</strong> Changes will create a new schema version. The form will automatically
						use the latest version.
					</p>
				</div>
			{:else}
				<!-- Debug: Schema not loaded -->
				<div
					style="margin-bottom: 16px; padding: 8px; background: #fee; border-radius: 4px; font-size: 12px;"
				>
					<strong>❌ Schema not loaded:</strong> editingSchema is null<br />
					<strong>formSchema:</strong>
					{formSchema ? 'loaded' : 'null'}<br />
					<strong>formSchema fields:</strong>
					{formSchema?.fields?.length || 0}<br />
					<strong>showManageFormModal:</strong>
					{showManageFormModal}
				</div>
				<p style="color: #666; font-style: italic;">Loading form schema...</p>
			{/if}
		</Modal>

		<!-- Manage Cargo Modal -->
		<Modal
			bind:open={showManageCargoModal}
			modalHeading="Manage Cargo Types"
			primaryButtonText={editingCargoType ? 'Save Changes' : 'Add Cargo Type'}
			secondaryButtonText="Cancel"
			on:click:button--secondary={() => {
				showManageCargoModal = false;
				editingCargoType = null;
				newCargoType = { id: '', nameEn: '', nameZh: '', description: '' };
			}}
			on:click:button--primary={editingCargoType ? saveEditedCargoType : addCargoType}
			primaryButtonDisabled={editingCargoType
				? !editingCargoType.id.trim() ||
					!editingCargoType.nameEn.trim() ||
					!editingCargoType.nameZh.trim() ||
					isLoading
				: !newCargoType.id.trim() ||
					!newCargoType.nameEn.trim() ||
					!newCargoType.nameZh.trim() ||
					isLoading}
			size="lg"
		>
			{#if editingCargoType}
				<!-- Edit Existing Cargo Type -->
				<div
					style="margin-bottom: 24px; padding: 16px; background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 6px;"
				>
					<h4 style="margin: 0 0 16px 0; color: #856404;">✏️ Edit Cargo Type</h4>
					<div style="margin-bottom: 16px;">
						<TextInput
							labelText="Cargo Type ID *"
							placeholder="e.g., 105, electronics, textiles"
							bind:value={editingCargoType.id}
							required
						/>
					</div>
					<div
						style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 16px;"
					>
						<TextInput
							labelText="Cargo Type Name (English) *"
							placeholder="e.g., Electronics, Textiles"
							bind:value={editingCargoType.nameEn}
							required
						/>
						<TextInput
							labelText="Cargo Type Name (Chinese) *"
							placeholder="e.g., 电子产品, 纺织品"
							bind:value={editingCargoType.nameZh}
							required
						/>
					</div>
					<div style="margin-bottom: 16px;">
						<TextArea
							labelText="Description (Optional)"
							placeholder="Additional details about this cargo type..."
							bind:value={editingCargoType.description}
							rows={3}
						/>
					</div>
					<Button kind="ghost" size="sm" on:click={cancelEditingCargoType}>Cancel Edit</Button>
				</div>
			{:else}
				<!-- Add New Cargo Type -->
				<div
					style="margin-bottom: 24px; padding: 16px; background: #e8f4fd; border: 1px solid #b3d9ff; border-radius: 6px;"
				>
					<h4 style="margin: 0 0 16px 0; color: #0066cc;">➕ Add New Cargo Type</h4>
					<div style="margin-bottom: 16px;">
						<TextInput
							labelText="Cargo Type ID *"
							placeholder="e.g., 105, electronics, textiles"
							bind:value={newCargoType.id}
							required
						/>
					</div>
					<div
						style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 16px;"
					>
						<TextInput
							labelText="Cargo Type Name (English) *"
							placeholder="e.g., Electronics, Textiles"
							bind:value={newCargoType.nameEn}
							required
						/>
						<TextInput
							labelText="Cargo Type Name (Chinese) *"
							placeholder="e.g., 电子产品, 纺织品"
							bind:value={newCargoType.nameZh}
							required
						/>
					</div>
					<div style="margin-bottom: 16px;">
						<TextArea
							labelText="Description (Optional)"
							placeholder="Additional details about this cargo type..."
							bind:value={newCargoType.description}
							rows={3}
						/>
					</div>
				</div>
			{/if}

			<div style="margin-top: 24px;">
				<h4>Current Cargo Types ({cargoTypes.length}):</h4>
				{#if cargoTypes.length > 0}
					<div
						style="max-height: 400px; overflow-y: auto; border: 1px solid #ddd; border-radius: 6px; margin: 8px 0;"
					>
						{#each cargoTypes as cargoType, index}
							<div
								style="padding: 16px; border-bottom: 1px solid #eee; {index ===
								cargoTypes.length - 1
									? 'border-bottom: none;'
									: ''}"
							>
								<div
									style="display: flex; justify-content: space-between; align-items: flex-start;"
								>
									<!-- Cargo Type Info -->
									<div style="flex: 1;">
										<div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
											<strong style="color: #333; font-size: 16px;">
												{cargoType.name?.en || cargoType.name || cargoType.label || 'Unknown'}
											</strong>
											<span
												style="background: #e3f2fd; color: #1976d2; padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight: 500;"
											>
												ID: {cargoType.id || cargoType.value}
											</span>
										</div>
										{#if cargoType.name?.zh}
											<div style="color: #666; margin-bottom: 4px; font-size: 14px;">
												中文: {cargoType.name.zh}
											</div>
										{/if}
										{#if cargoType.description}
											<div style="color: #666; font-size: 12px; font-style: italic;">
												{cargoType.description}
											</div>
										{/if}
									</div>

									<!-- Action Buttons -->
									<div style="display: flex; align-items: center; gap: 8px; margin-left: 16px;">
										<Button
											kind="tertiary"
											size="sm"
											on:click={() => startEditingCargoType(cargoType)}
											disabled={isLoading}
											title="Edit cargo type"
										>
											✏️ Edit
										</Button>
										<Button
											kind="danger-ghost"
											size="sm"
											on:click={() => deleteCargoType(cargoType.id || cargoType.value)}
											disabled={isLoading}
											title="Delete cargo type"
										>
											🗑️ Delete
										</Button>
									</div>
								</div>
							</div>
						{/each}
					</div>
				{:else}
					<div
						style="text-align: center; padding: 16px; background: #f9f9f9; border-radius: 4px; margin: 8px 0;"
					>
						<div style="font-size: 24px; margin-bottom: 8px;">🚢</div>
						<p style="margin: 0; color: #666;">No cargo types found</p>
						<p style="margin: 4px 0 0 0; font-size: 12px; color: #999;">
							Check console for API errors
						</p>
					</div>
				{/if}
			</div>

			<!-- Info Section -->
			<div
				style="margin-top: 16px; padding: 12px; background: #f0f8ff; border: 1px solid #b3d9ff; border-radius: 4px;"
			>
				<div style="font-size: 14px; color: #0066cc;">
					<strong>💡 Cargo Type Management:</strong>
					<ul style="margin: 8px 0 0 20px; font-size: 12px;">
						<li>Each cargo type requires a unique ID, English name, and Chinese name</li>
						<li>IDs are used in form submissions and should be consistent</li>
						<li>Use the Edit button to modify existing cargo types</li>
						<li>Changes will be reflected in the form dropdown immediately</li>
					</ul>
				</div>
			</div>
		</Modal>

		<!-- Manage Team Modal -->
		<Modal
			bind:open={showManageTeamModal}
			modalHeading="Manage Team Members"
			primaryButtonText="Add Member"
			secondaryButtonText="Cancel"
			on:click:button--secondary={() => (showManageTeamModal = false)}
			on:click:button--primary={addTeamMember}
			primaryButtonDisabled={!newTeamMember.email.trim() || isLoadingTeam}
			size="lg"
		>
			<!-- Add New Member Section -->
			<div style="margin-bottom: 24px; padding: 16px; background: #e8f4fd; border-radius: 6px;">
				<h4 style="margin: 0 0 16px 0;">➕ Add New Team Member</h4>
				<div style="display: grid; grid-template-columns: 2fr 1fr; gap: 12px; margin-bottom: 12px;">
					<TextInput
						type="email"
						labelText="Email Address *"
						placeholder="new.member@dock2gdansk.com"
						bind:value={newTeamMember.email}
						disabled={isLoadingTeam}
						invalid={newTeamMember.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(newTeamMember.email)}
						invalidText="Please enter a valid email address"
					/>
					<Select labelText="Role *" bind:selected={newTeamMember.role} disabled={isLoadingTeam}>
						<SelectItem value="admin" text="Administrator" />
						<SelectItem value="manager" text="Manager" />
						<SelectItem value="viewer" text="Viewer" />
					</Select>
				</div>
			</div>

			<!-- Current Team Members Section -->
			<div style="margin-bottom: 16px;">
				<h4>Current Team Members ({teamMembers.length})</h4>
				{#if isLoadingTeam}
					<div style="text-align: center; padding: 32px; color: #666;">
						<div style="font-size: 24px; margin-bottom: 8px;">⏳</div>
						<p style="margin: 0;">Loading team members...</p>
					</div>
				{:else if teamMembers.length > 0}
					<div
						style="max-height: 400px; overflow-y: auto; border: 1px solid #ddd; border-radius: 6px; margin-top: 8px;"
					>
						{#each teamMembers as member, index}
							<div
								style="padding: 16px; border-bottom: 1px solid #eee; {index ===
								teamMembers.length - 1
									? 'border-bottom: none;'
									: ''}"
							>
								<div style="display: flex; justify-content: between; align-items: center;">
									<!-- Member Info -->
									<div style="flex: 1;">
										<div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
											<strong style="color: #333;">{member.email}</strong>
											{#if member.email === adminEmail}
												<span
													style="background: #e3f2fd; color: #1976d2; padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight: 500;"
												>
													You
												</span>
											{/if}
											<span
												style="background: #f3e5f5; color: #7b1fa2; padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight: 500;"
											>
												{member.role || 'Admin'}
											</span>
											{#if member.status === 'PENDING'}
												<span
													style="background: #fff3cd; color: #856404; padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight: 500;"
												>
													Pending
												</span>
											{:else if member.status === 'CONFIRMED'}
												<span
													style="background: #d4edda; color: #155724; padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight: 500;"
												>
													Active
												</span>
											{/if}
										</div>
										<div style="font-size: 12px; color: #666;">
											{#if member.dateCreated}
												Added: {new Date(member.dateCreated).toLocaleDateString()}
											{/if}
											{#if member.lastLogin}
												• Last login: {new Date(member.lastLogin).toLocaleDateString()}
											{/if}
										</div>
									</div>

									<!-- Member Actions -->
									<div style="display: flex; align-items: center; gap: 8px;">
										<!-- Role Selector -->
										{#if member.email !== adminEmail}
											<Select
												size="sm"
												bind:selected={member.role}
												on:change={(e) => updateTeamMemberRole(member.email, e.target.value)}
												disabled={isLoadingTeam}
												style="min-width: 120px;"
											>
												<SelectItem value="admin" text="Administrator" />
												<SelectItem value="manager" text="Manager" />
												<SelectItem value="viewer" text="Viewer" />
											</Select>
										{/if}

										<!-- Remove Button -->
										{#if member.email !== adminEmail}
											<Button
												kind="danger-ghost"
												size="sm"
												on:click={() => removeTeamMember(member.email)}
												disabled={isLoadingTeam}
												title="Remove team member"
											>
												🗑️
											</Button>
										{:else}
											<div
												style="width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; color: #ccc;"
												title="Cannot remove yourself"
											>
												🔒
											</div>
										{/if}
									</div>
								</div>
							</div>
						{/each}
					</div>
				{:else}
					<div style="text-align: center; padding: 32px; color: #666;">
						<div style="font-size: 24px; margin-bottom: 8px;">👥</div>
						<p style="margin: 0;">No team members found</p>
						<p style="margin: 4px 0 0 0; font-size: 12px; color: #999;">
							Add team members using the form above
						</p>
					</div>
				{/if}
			</div>

			<!-- Info Section -->
			<div
				style="margin-top: 16px; padding: 12px; background: #f0f8ff; border: 1px solid #b3d9ff; border-radius: 4px;"
			>
				<div style="font-size: 14px; color: #0066cc;">
					<strong>💡 Team Management:</strong>
					<ul style="margin: 8px 0 0 20px; font-size: 12px;">
						<li>Administrators can manage all team members and system settings</li>
						<li>Managers can view and export data, but cannot modify settings</li>
						<li>Viewers can only view dashboard and submission data</li>
						<li>Team members are managed through AWS Cognito user pool</li>
					</ul>
				</div>
			</div>
		</Modal>

		<!-- Manage Analysis Emails Modal -->
		<Modal
			bind:open={showManageEmailsModal}
			modalHeading="Manage Analysis Email Recipients"
			primaryButtonText="Add Email"
			secondaryButtonText="Cancel"
			on:click:button--secondary={() => (showManageEmailsModal = false)}
			on:click:button--primary={addClientEmail}
			primaryButtonDisabled={!newEmail.trim() ||
				isLoadingEmails ||
				!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(newEmail)}
			size="lg"
		>
			<!-- Add New Email Section -->
			<div style="margin-bottom: 24px; padding: 16px; background: #e8f4fd; border-radius: 6px;">
				<h4 style="margin: 0 0 16px 0;">📧 Add New Email Recipient</h4>
				<div style="margin-bottom: 12px;">
					<TextInput
						type="email"
						labelText="Email Address *"
						placeholder="client@example.com"
						bind:value={newEmail}
						disabled={isLoadingEmails}
						invalid={newEmail && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(newEmail)}
						invalidText="Please enter a valid email address"
					/>
				</div>
				<div
					style="margin-top: 8px; padding: 8px; background: rgba(0,0,0,0.05); border-radius: 4px; font-size: 12px; color: #666;"
				>
					<strong>Purpose:</strong> These emails will receive analysis reports and notifications about
					form submissions for further review.
				</div>
			</div>

			<!-- Current Email Recipients Section -->
			<div style="margin-bottom: 16px;">
				<h4>Current Email Recipients ({clientEmails.length})</h4>
				{#if isLoadingEmails}
					<div style="text-align: center; padding: 32px; color: #666;">
						<div style="font-size: 24px; margin-bottom: 8px;">⏳</div>
						<p style="margin: 0;">Loading email recipients...</p>
					</div>
				{:else if clientEmails.length > 0}
					<div
						style="max-height: 400px; overflow-y: auto; border: 1px solid #ddd; border-radius: 6px; margin-top: 8px;"
					>
						{#each clientEmails as email, index}
							<div
								style="padding: 16px; border-bottom: 1px solid #eee; {index ===
								clientEmails.length - 1
									? 'border-bottom: none;'
									: ''}"
							>
								<div style="display: flex; justify-content: space-between; align-items: center;">
									<!-- Email Info -->
									<div style="flex: 1;">
										<div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
											<strong style="color: #333;">{email.email}</strong>
											{#if email.name && email.name !== email.email.split('@')[0]}
												<span style="color: #666;">({email.name})</span>
											{/if}
											<span
												style="background: {email.active
													? '#d4edda'
													: '#f8d7da'}; color: {email.active
													? '#155724'
													: '#721c24'}; padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight: 500;"
											>
												{email.active ? 'Active' : 'Inactive'}
											</span>
										</div>
										<div style="font-size: 12px; color: #666;">
											{#if email.addedAt}
												Added: {new Date(email.addedAt).toLocaleDateString()}
											{/if}
										</div>
									</div>

									<!-- Email Actions -->
									<div style="display: flex; align-items: center; gap: 8px;">
										<!-- Toggle Active Status -->
										<Button
											kind={email.active ? 'ghost' : 'tertiary'}
											size="sm"
											on:click={() => toggleEmailStatus(email.id, !email.active)}
											disabled={isLoadingEmails}
											title={email.active ? 'Deactivate email' : 'Activate email'}
										>
											{email.active ? '⏸️' : '▶️'}
										</Button>

										<!-- Remove Button -->
										<Button
											kind="danger-ghost"
											size="sm"
											on:click={() => removeClientEmail(email)}
											disabled={isLoadingEmails}
											title="Remove email recipient"
										>
											🗑️
										</Button>
									</div>
								</div>
							</div>
						{/each}
					</div>
				{:else}
					<div style="text-align: center; padding: 32px; color: #666;">
						<div style="font-size: 24px; margin-bottom: 8px;">📧</div>
						<p style="margin: 0;">No email recipients configured</p>
						<p style="margin: 4px 0 0 0; font-size: 12px; color: #999;">
							Add email addresses using the form above
						</p>
					</div>
				{/if}
			</div>

			<!-- Info Section -->
			<div
				style="margin-top: 16px; padding: 12px; background: #f0f8ff; border: 1px solid #b3d9ff; border-radius: 4px;"
			>
				<div style="font-size: 14px; color: #0066cc;">
					<strong>💡 Analysis Email Management:</strong>
					<ul style="margin: 8px 0 0 20px; font-size: 12px;">
						<li>Active recipients receive notifications about new form submissions</li>
						<li>Inactive recipients are temporarily excluded from notifications</li>
						<li>Analysis reports include submission trends and insights</li>
						<li>Default recipients: Marek.Machalski@portgdansk.pl and michal@dagodigital.com</li>
					</ul>
				</div>
			</div>
		</Modal>

		<!-- New User Credentials Modal -->
		<Modal
			bind:open={showCredentials}
			modalHeading="✅ Team Member Added Successfully"
			primaryButtonText="Copy Credentials"
			secondaryButtonText="Close"
			on:click:button--secondary={() => {
				showCredentials = false;
				newUserCredentials = null;
			}}
			on:click:button--primary={copyCredentials}
			size="md"
		>
			{#if newUserCredentials}
				<div style="margin-bottom: 24px;">
					<p
						style="margin-bottom: 16px; color: #155724; background: #d4edda; padding: 12px; border-radius: 4px; font-weight: 500;"
					>
						✅ New team member has been successfully added to the system!
					</p>

					<div
						style="background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 6px; padding: 16px; font-family: monospace;"
					>
						<h4 style="margin: 0 0 12px 0; color: #333;">Login Credentials:</h4>
						<div style="line-height: 1.6;">
							<strong>Email:</strong>
							{newUserCredentials.email}<br />
							<strong>Temporary Password:</strong>
							{newUserCredentials.temporaryPassword}<br />
							<strong>Login URL:</strong>
							{newUserCredentials.loginUrl}
						</div>
					</div>

					<div
						style="margin-top: 16px; padding: 12px; background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 4px;"
					>
						<p style="margin: 0; font-size: 14px; color: #856404;">
							<strong>⚠️ Important:</strong>
						</p>
						<ul style="margin: 8px 0 0 20px; font-size: 12px; color: #856404;">
							<li>Share these credentials securely with the new team member</li>
							<li>They will be required to change their password on first login</li>
							<li>No automatic invitation email was sent</li>
						</ul>
					</div>
				</div>
			{/if}
		</Modal>

		<!-- Manage Sources Modal -->
		<Modal
			bind:open={showManageSourcesModal}
			modalHeading="Manage Referral Sources"
			primaryButtonText={editingSource ? 'Save Changes' : 'Add Source'}
			secondaryButtonText="Cancel"
			on:click:button--secondary={() => {
				showManageSourcesModal = false;
				editingSource = null;
				newSource = { id: '', nameEn: '', nameZh: '', description: '' };
			}}
			on:click:button--primary={editingSource ? saveEditedSource : addReferralSource}
			primaryButtonDisabled={editingSource
				? !editingSource.id.trim() ||
					!editingSource.nameEn.trim() ||
					!editingSource.nameZh.trim() ||
					isLoadingSources
				: !newSource.id.trim() ||
					!newSource.nameEn.trim() ||
					!newSource.nameZh.trim() ||
					isLoadingSources}
			size="lg"
		>
			{#if editingSource}
				<!-- Edit Existing Source -->
				<div
					style="margin-bottom: 24px; padding: 16px; background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 6px;"
				>
					<h4 style="margin: 0 0 16px 0; color: #856404;">✏️ Edit Referral Source</h4>
					<div style="margin-bottom: 16px;">
						<TextInput
							labelText="Source ID *"
							placeholder="e.g., google, facebook, clif_2025"
							bind:value={editingSource.id}
							required
						/>
					</div>
					<div
						style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 16px;"
					>
						<TextInput
							labelText="Source Name (English) *"
							placeholder="e.g., Google Search, Facebook Ad"
							bind:value={editingSource.nameEn}
							required
						/>
						<TextInput
							labelText="Source Name (Chinese) *"
							placeholder="e.g., 谷歌搜索, 脸书广告"
							bind:value={editingSource.nameZh}
							required
						/>
					</div>
					<div style="margin-bottom: 16px;">
						<TextArea
							labelText="Description (Optional)"
							placeholder="Additional details about this referral source..."
							bind:value={editingSource.description}
							rows={3}
						/>
					</div>
					<Button kind="ghost" size="sm" on:click={cancelEditingSource}>Cancel Edit</Button>
				</div>
			{:else}
				<!-- Add New Source -->
				<div
					style="margin-bottom: 24px; padding: 16px; background: #e8f4fd; border: 1px solid #b3d9ff; border-radius: 6px;"
				>
					<h4 style="margin: 0 0 16px 0; color: #0066cc;">➕ Add New Referral Source</h4>
					<div style="margin-bottom: 16px;">
						<TextInput
							labelText="Source ID *"
							placeholder="e.g., google, facebook, clif_2025"
							bind:value={newSource.id}
							required
						/>
					</div>
					<div
						style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 16px;"
					>
						<TextInput
							labelText="Source Name (English) *"
							placeholder="e.g., Google Search, Facebook Ad"
							bind:value={newSource.nameEn}
							required
						/>
						<TextInput
							labelText="Source Name (Chinese) *"
							placeholder="e.g., 谷歌搜索, 脸书广告"
							bind:value={newSource.nameZh}
							required
						/>
					</div>
					<div style="margin-bottom: 16px;">
						<TextArea
							labelText="Description (Optional)"
							placeholder="Additional details about this referral source..."
							bind:value={newSource.description}
							rows={3}
						/>
					</div>
				</div>
			{/if}

			<div style="margin-top: 24px;">
				<h4>Current Referral Sources ({referralSources.length}):</h4>
				{#if referralSources.length > 0}
					<div
						style="max-height: 400px; overflow-y: auto; border: 1px solid #ddd; border-radius: 6px; margin: 8px 0;"
					>
						{#each referralSources as source, index}
							<div
								style="padding: 16px; border-bottom: 1px solid #eee; {index ===
								referralSources.length - 1
									? 'border-bottom: none;'
									: ''}"
							>
								<div
									style="display: flex; justify-content: space-between; align-items: flex-start;"
								>
									<!-- Source Info -->
									<div style="flex: 1;">
										<div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
											<strong style="color: #333; font-size: 16px;">
												{source.name?.en || source.name || source.label || 'Unknown'}
											</strong>
											<span
												style="background: #e3f2fd; color: #1976d2; padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight: 500;"
											>
												ID: {source.id || source.value}
											</span>
										</div>
										{#if source.name?.zh}
											<div style="color: #666; margin-bottom: 4px; font-size: 14px;">
												中文: {source.name.zh}
											</div>
										{/if}
										{#if source.description}
											<div style="color: #666; font-size: 12px; font-style: italic;">
												{source.description}
											</div>
										{/if}
									</div>

									<!-- Action Buttons -->
									<div style="display: flex; align-items: center; gap: 8px; margin-left: 16px;">
										<Button
											kind="tertiary"
											size="sm"
											on:click={() => startEditingSource(source)}
											disabled={isLoadingSources}
											title="Edit referral source"
										>
											✏️ Edit
										</Button>
										<Button
											kind="danger-ghost"
											size="sm"
											on:click={() => deleteReferralSource(source.id || source.value)}
											disabled={isLoadingSources}
											title="Delete referral source"
										>
											🗑️ Delete
										</Button>
									</div>
								</div>
							</div>
						{/each}
					</div>
				{:else}
					<div
						style="text-align: center; padding: 16px; background: #f9f9f9; border-radius: 4px; margin: 8px 0;"
					>
						<div style="font-size: 24px; margin-bottom: 8px;">📍</div>
						<p style="margin: 0; color: #666;">No referral sources found</p>
						<p style="margin: 4px 0 0 0; font-size: 12px; color: #999;">
							Check console for API errors
						</p>
					</div>
				{/if}
			</div>

			<!-- Info Section -->
			<div
				style="margin-top: 16px; padding: 12px; background: #f0f8ff; border: 1px solid #b3d9ff; border-radius: 4px;"
			>
				<div style="font-size: 14px; color: #0066cc;">
					<strong>💡 Referral Source Management:</strong>
					<ul style="margin: 8px 0 0 20px; font-size: 12px;">
						<li>Each source requires a unique ID, English name, and Chinese name</li>
						<li>Sources appear in the "Where did you hear about us?" dropdown</li>
						<li>Use the Edit button to modify existing sources</li>
						<li>Changes will be reflected in the form dropdown immediately</li>
					</ul>
				</div>
			</div>
		</Modal>
	</div>
{:else}
	<div class="flex min-h-screen items-center justify-center">
		<div class="text-center">
			<div class="mb-4 text-6xl text-gray-400">📊</div>
			<p class="text-gray-600">Loading dashboard...</p>
		</div>
	</div>
{/if}

<style>
	:global(.bx--clickable-tile) {
		min-height: 120px;
	}

	:global(.bx--data-table-container) {
		background: white;
	}

	/* Dashboard Container */
	.dashboard-container {
		max-width: 84rem;
		margin: 0 auto;
		padding: 24px;
		margin-top: 64px;
	}

	.header-section {
		margin-bottom: 24px;
	}

	.header-content {
		display: flex;
		justify-content: space-between;
		align-items: center;
		margin-top: 16px;
	}

	.header-info {
		flex: 1;
	}

	.dashboard-title {
		font-size: 28px;
		font-weight: bold;
		margin-bottom: 8px;
		color: #333;
	}

	.welcome-text {
		color: #666;
		margin-bottom: 32px;
	}

	/* Dashboard Layout */
	.dashboard-row {
		display: flex;
		gap: 24px;
		margin-bottom: 48px;
	}

	.dashboard-column {
		flex: 1;
		min-width: 0; /* Prevents flex items from overflowing */
	}

	.tile-padding {
		padding: 24px;
	}

	.section-title {
		font-size: 20px;
		font-weight: 600;
		margin-bottom: 16px;
		color: #333;
	}

	/* Button Grid */
	.button-grid {
		display: grid;
		gap: 12px;
		grid-template-columns: 1fr;
	}

	@media (min-width: 768px) {
		.button-grid {
			grid-template-columns: repeat(2, 1fr);
			gap: 16px;
		}
	}

	@media (min-width: 1024px) {
		.button-grid {
			grid-template-columns: repeat(4, 1fr);
		}
	}

	.action-button {
		width: 100%;
	}

	/* Status List */
	.status-list {
		display: flex;
		flex-direction: column;
		gap: 16px;
	}

	.status-item {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	.status-label {
		font-size: 14px;
		color: #666;
	}

	.status-indicator {
		width: 24px;
		height: 24px;
		border-radius: 50%;
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 12px;
		font-weight: bold;
	}

	.status-ok {
		background-color: #22c55e;
		color: white;
	}

	.status-error {
		background-color: #ef4444;
		color: white;
	}

	/* Submissions */
	.submissions-tile {
		padding: 24px;
		margin-top: 24px;
	}

	/* Responsive Design */
	@media (max-width: 768px) {
		.dashboard-row {
			flex-direction: column;
			gap: 16px;
			margin-bottom: 32px;
		}

		.button-grid {
			flex-direction: column;
		}
	}
</style>
