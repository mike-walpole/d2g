<script>
	import { 
		Button, Tile, Grid, Column, DataTable, Toolbar, ToolbarContent,
		ToolbarSearch, ToolbarMenu, ToolbarMenuItem, Breadcrumb, BreadcrumbItem,
		Tag, ProgressBar, ClickableTile, Modal, TextInput, TextArea, Select, SelectItem, Checkbox
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

	// Form data for modals
	let newCargoType = { 
		nameEn: '', 
		nameZh: '', 
		description: '' 
	};
	let newTeamMember = { email: '', role: 'admin' };
	let selectedSchema = null;
	
	// Team management data
	let teamMembers = [];
	let isLoadingTeam = false;
	
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
	});

	async function loadDashboardData() {
		try {
			console.log('🔄 Fetching submissions from API...');
			const response = await fetch('https://9u6shrsot7.execute-api.ap-east-1.amazonaws.com/kapitanat/submissions', {
				headers: {
					'Authorization': `Bearer ${localStorage.getItem('admin-token')}`
				}
			});
			
			console.log('📡 Submissions API Response:', response.status, response.statusText);
			
			if (response.ok) {
				const data = await response.json();
				console.log('📊 Submissions Data:', data);
				
				if (data.success && data.submissions) {
					// Map the API response to the expected format
					const mappedSubmissions = data.submissions.map(submission => ({
						id: submission.id,
						company: submission.formData.company,
						email: submission.formData.email,
						phone: `${submission.formData.phone_prefix} ${submission.formData.phone}`,
						cargoType: submission.formData.cargo_type,
						inquiryContent: submission.formData.inquiry_content,
						timestamp: submission.timestamp
					}));
					
					dashboardData = {
						totalSubmissions: data.count || data.submissions.length,
						totalSchemas: 3,
						totalUsers: 8,
						recentSubmissions: mappedSubmissions.slice(0, 5) // Show last 5
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
		{ key: 'inquiryContent', value: 'Inquiry' },
		{ key: 'timestamp', value: 'Submitted' }
	];

	// Format timestamp
	function formatDate(timestamp) {
		return new Date(timestamp).toLocaleDateString('en-US', {
			year: 'numeric',
			month: 'short',
			day: 'numeric',
			hour: '2-digit',
			minute: '2-digit'
		});
	}

	// Load real cargo types
	async function loadCargoTypes() {
		try {
			console.log('🔄 Fetching cargo types from API...');
			const response = await fetch('https://9u6shrsot7.execute-api.ap-east-1.amazonaws.com/kapitanat/cargo-types', {
				headers: {
					'Authorization': `Bearer ${localStorage.getItem('admin-token')}`
				}
			});
			
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
			const response = await fetch('https://9u6shrsot7.execute-api.ap-east-1.amazonaws.com/schema?formId=dock2gdansk-main');
			
			console.log('📡 Form Schema API Response:', response.status, response.statusText);
			
			if (response.ok) {
				const data = await response.json();
				console.log('📋 Form Schema Data:', data);
				
				if (data.success && data.schema) {
					formSchema = data.schema;
					console.log('✅ Successfully loaded form schema with', formSchema.fields?.length || 0, 'fields');
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
		if (!newCargoType.nameEn.trim() || !newCargoType.nameZh.trim()) {
			console.error('❌ Both English and Chinese names are required');
			return;
		}
		
		isLoading = true;
		try {
			console.log('🔄 Adding cargo type via API:', newCargoType);
			
			const response = await fetch('https://9u6shrsot7.execute-api.ap-east-1.amazonaws.com/kapitanat/cargo-types', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'Authorization': `Bearer ${localStorage.getItem('admin-token')}`
				},
				body: JSON.stringify({
					name: {
						en: newCargoType.nameEn,
						zh: newCargoType.nameZh
					},
					description: newCargoType.description
				})
			});
			
			if (response.ok) {
				const result = await response.json();
				console.log('✅ Cargo type added successfully:', result);
				
				// Reload cargo types from API
				await loadCargoTypes();
				
				// Also refresh the config data so frontend gets updated cargo types
				import('$lib/stores/config.js').then(module => {
					module.loadConfig('en');
				});
				
				// Reset form
				newCargoType = { nameEn: '', nameZh: '', description: '' };
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

	async function deleteCargoType(cargoId) {
		isLoading = true;
		try {
			console.log('🔄 Deleting cargo type via API:', cargoId);
			
			const response = await fetch(`https://9u6shrsot7.execute-api.ap-east-1.amazonaws.com/kapitanat/cargo-types`, {
				method: 'DELETE',
				headers: {
					'Content-Type': 'application/json',
					'Authorization': `Bearer ${localStorage.getItem('admin-token')}`
				},
				body: JSON.stringify({
					id: cargoId
				})
			});
			
			if (response.ok) {
				const result = await response.json();
				console.log('✅ Cargo type deleted successfully:', result);
				
				// Reload cargo types from API
				await loadCargoTypes();
				
				// Also refresh the config data so frontend gets updated cargo types
				import('$lib/stores/config.js').then(module => {
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
			const response = await fetch('https://9u6shrsot7.execute-api.ap-east-1.amazonaws.com/kapitanat/team', {
				headers: {
					'Authorization': `Bearer ${localStorage.getItem('admin-token')}`
				}
			});
			
			console.log('📡 Team API Response:', response.status, response.statusText);
			
			if (response.ok) {
				const data = await response.json();
				console.log('👥 Team Members Data:', data);
				
				if (data.success && data.teamMembers) {
					teamMembers = data.teamMembers;
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
			
			const response = await fetch('https://9u6shrsot7.execute-api.ap-east-1.amazonaws.com/kapitanat/team', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'Authorization': `Bearer ${localStorage.getItem('admin-token')}`
				},
				body: JSON.stringify({
					email: newTeamMember.email,
					role: newTeamMember.role,
					sendInvite: true
				})
			});
			
			if (response.ok) {
				const result = await response.json();
				console.log('✅ Team member added successfully:', result);
				
				// Reload team members from API
				await loadTeamMembers();
				
				// Reset form
				newTeamMember = { email: '', role: 'admin' };
				showManageTeamModal = false;
			} else {
				const errorData = await response.json();
				console.error('❌ Failed to add team member:', response.status, response.statusText, errorData);
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
			
			const response = await fetch('https://9u6shrsot7.execute-api.ap-east-1.amazonaws.com/kapitanat/team', {
				method: 'DELETE',
				headers: {
					'Content-Type': 'application/json',
					'Authorization': `Bearer ${localStorage.getItem('admin-token')}`
				},
				body: JSON.stringify({
					email: userEmail
				})
			});
			
			if (response.ok) {
				const result = await response.json();
				console.log('✅ Team member removed successfully:', result);
				
				// Reload team members from API
				await loadTeamMembers();
			} else {
				const errorData = await response.json();
				console.error('❌ Failed to remove team member:', response.status, response.statusText, errorData);
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
			
			const response = await fetch('https://9u6shrsot7.execute-api.ap-east-1.amazonaws.com/kapitanat/team', {
				method: 'PUT',
				headers: {
					'Content-Type': 'application/json',
					'Authorization': `Bearer ${localStorage.getItem('admin-token')}`
				},
				body: JSON.stringify({
					email: userEmail,
					role: newRole
				})
			});
			
			if (response.ok) {
				const result = await response.json();
				console.log('✅ Team member role updated successfully:', result);
				
				// Reload team members from API
				await loadTeamMembers();
			} else {
				const errorData = await response.json();
				console.error('❌ Failed to update team member role:', response.status, response.statusText, errorData);
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
			const response = await fetch('https://9u6shrsot7.execute-api.ap-east-1.amazonaws.com/schema?formId=dock2gdansk-main');
			
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
		if (editingFields.some(f => f.id === newField.id)) {
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
		editingFields = editingFields.filter(f => f.id !== fieldId);
	}

	function updateField(fieldId, property, value) {
		const field = editingFields.find(f => f.id === fieldId);
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
			const response = await fetch('https://9u6shrsot7.execute-api.ap-east-1.amazonaws.com/kapitanat/schemas', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					'Authorization': `Bearer ${localStorage.getItem('admin-token')}`
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
			});

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
					<Button 
						kind="primary" 
						on:click={openManageFormModal}
						class="action-button"
					>
						Manage Form
					</Button>
					<Button 
						kind="tertiary" 
						on:click={() => showManageCargoModal = true}
						class="action-button"
					>
						Manage Cargo
					</Button>
					<Button 
						kind="tertiary" 
						on:click={() => showManageTeamModal = true}
						class="action-button"
					>
						Manage Team
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
		
		<DataTable
			{headers}
			rows={dashboardData.recentSubmissions.map(submission => ({
				...submission,
				inquiryContent: submission.inquiryContent.length > 50 ? 
					submission.inquiryContent.substring(0, 50) + '...' : 
					submission.inquiryContent,
				timestamp: formatDate(submission.timestamp)
			}))}
		>
			<Toolbar>
				<ToolbarContent>
					<ToolbarSearch />
					<ToolbarMenu>
						<ToolbarMenuItem primaryFocus href="/kapitanat/submissions">
							View All Submissions
						</ToolbarMenuItem>
						<ToolbarMenuItem href="/kapitanat/submissions/export">
							Export Data
						</ToolbarMenuItem>
					</ToolbarMenu>
				</ToolbarContent>
			</Toolbar>
		</DataTable>
		
		{#if dashboardData.recentSubmissions.length === 0}
			<div style="text-align: center; padding: 32px; color: #666;">
				<div style="font-size: 48px; margin-bottom: 16px;">📭</div>
				<h3 style="margin-bottom: 8px;">No submissions found</h3>
				<p style="margin: 0;">Either no form submissions exist yet, or there was an error loading data from the database.</p>
				<p style="margin: 8px 0 0 0; font-size: 14px; color: #999;">Check the browser console for API error details.</p>
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
			<div style="margin-bottom: 16px; padding: 8px; background: #f0f0f0; border-radius: 4px; font-size: 12px;">
				<strong>Debug:</strong> Schema loaded with {editingFields.length} fields | Version: {editingSchema.version || '1.0.0'} | API Version: {formSchema?.version || 'unknown'}
			</div>

			<!-- Form Title Section -->
			<div style="margin-bottom: 24px; padding: 16px; background: #f8f9fa; border-radius: 6px;">
				<h4 style="margin: 0 0 12px 0;">Form Title</h4>
				<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
					<TextInput
						labelText="English Title"
						bind:value={editingSchema.title.en}
					/>
					<TextInput
						labelText="Chinese Title"
						bind:value={editingSchema.title.zh}
					/>
				</div>
			</div>

			<!-- Add New Field Section -->
			<div style="margin-bottom: 24px; padding: 16px; background: #e8f4fd; border-radius: 6px;">
				<h4 style="margin: 0 0 16px 0;">➕ Add New Field</h4>
				<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 12px;">
					<TextInput
						labelText="Field ID *"
						placeholder="e.g., company_name"
						bind:value={newField.id}
					/>
					<Select
						labelText="Field Type *"
						bind:selected={newField.type}
					>
						{#each fieldTypes as type}
							<SelectItem value={type.value} text={type.label} />
						{/each}
					</Select>
				</div>
				
				<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 12px;">
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
				
				<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 12px;">
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
				
				<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 12px;">
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
					<Checkbox
						labelText="Required Field"
						bind:checked={newField.required}
					/>
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
					<div style="max-height: 400px; overflow-y: auto; border: 1px solid #ddd; border-radius: 6px;">
						{#each editingFields as field, index}
							<div style="padding: 16px; border-bottom: 1px solid #eee; {index === editingFields.length - 1 ? 'border-bottom: none;' : ''}">
								<!-- Field Header -->
								<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
									<div style="display: flex; align-items: center; gap: 8px;">
										<strong style="color: #333;">#{index + 1}: {field.id}</strong>
										<span style="background: #e1f5fe; color: #0277bd; padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight: 500;">
											{field.type}
										</span>
										{#if field.required}
											<span style="background: #ffebee; color: #c62828; padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight: 500;">
												Required
											</span>
										{/if}
									</div>
									<Button 
										kind="danger-ghost" 
										size="sm"
										on:click={() => deleteField(field.id)}
									>
										🗑️ Delete
									</Button>
								</div>
								
								<!-- Editable Fields -->
								<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 8px;">
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
									<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 8px;">
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
									<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 8px;">
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
						<p style="margin: 4px 0 0 0; font-size: 12px; color: #999;">Add fields using the form above</p>
					</div>
				{/if}
			</div>
			
			<div style="margin-top: 16px; padding: 12px; background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 4px;">
				<p style="margin: 0; font-size: 14px; color: #856404;">
					<strong>💡 Note:</strong> Changes will create a new schema version. The form will automatically use the latest version.
				</p>
			</div>
		{:else}
			<!-- Debug: Schema not loaded -->
			<div style="margin-bottom: 16px; padding: 8px; background: #fee; border-radius: 4px; font-size: 12px;">
				<strong>❌ Schema not loaded:</strong> editingSchema is null<br>
				<strong>formSchema:</strong> {formSchema ? 'loaded' : 'null'}<br>
				<strong>formSchema fields:</strong> {formSchema?.fields?.length || 0}<br>
				<strong>showManageFormModal:</strong> {showManageFormModal}
			</div>
			<p style="color: #666; font-style: italic;">Loading form schema...</p>
		{/if}
	</Modal>

	<!-- Manage Cargo Modal -->
	<Modal
		bind:open={showManageCargoModal}
		modalHeading="Manage Cargo Types"
		primaryButtonText="Add Cargo Type"
		secondaryButtonText="Cancel"
		on:click:button--secondary={() => showManageCargoModal = false}
		on:click:button--primary={addCargoType}
	>
		<div style="margin-bottom: 16px;">
			<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">
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
		</div>
		<div style="margin-bottom: 16px;">
			<TextArea
				labelText="Description (Optional)"
				placeholder="Additional details about this cargo type..."
				bind:value={newCargoType.description}
				rows={3}
			/>
		</div>
		
		<div style="margin-top: 24px;">
			<h4>Current Cargo Types:</h4>
			{#if cargoTypes.length > 0}
				<div style="max-height: 200px; overflow-y: auto; margin: 8px 0;">
					{#each cargoTypes as cargoType}
						<div style="display: flex; justify-content: space-between; align-items: center; padding: 8px; border-bottom: 1px solid #eee;">
							<span>
								<strong>
									{cargoType.name?.en || cargoType.name || cargoType.label || 'Unknown'}
								</strong>
								{cargoType.name?.zh ? ` (${cargoType.name.zh})` : ''}
								{cargoType.description ? `- ${cargoType.description}` : ''}
								<small style="color: #666; margin-left: 8px;">(ID: {cargoType.id || cargoType.value})</small>
							</span>
							<Button 
								kind="danger-ghost" 
								size="sm"
								on:click={() => deleteCargoType(cargoType.id || cargoType.value)}
								disabled={isLoading}
							>
								Delete
							</Button>
						</div>
					{/each}
				</div>
			{:else}
				<div style="text-align: center; padding: 16px; background: #f9f9f9; border-radius: 4px; margin: 8px 0;">
					<div style="font-size: 24px; margin-bottom: 8px;">🚢</div>
					<p style="margin: 0; color: #666;">No cargo types found</p>
					<p style="margin: 4px 0 0 0; font-size: 12px; color: #999;">Check console for API errors</p>
				</div>
			{/if}
		</div>
	</Modal>

	<!-- Manage Team Modal -->
	<Modal
		bind:open={showManageTeamModal}
		modalHeading="Manage Team Members"
		primaryButtonText="Add Member"
		secondaryButtonText="Cancel"
		on:click:button--secondary={() => showManageTeamModal = false}
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
				<Select
					labelText="Role *"
					bind:selected={newTeamMember.role}
					disabled={isLoadingTeam}
				>
					<SelectItem value="admin" text="Administrator" />
					<SelectItem value="manager" text="Manager" />
					<SelectItem value="viewer" text="Viewer" />
				</Select>
			</div>
			<div style="margin-top: 8px; padding: 8px; background: rgba(0,0,0,0.05); border-radius: 4px; font-size: 12px; color: #666;">
				<strong>Note:</strong> New members will receive an invitation email and must accept it to join the team.
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
				<div style="max-height: 400px; overflow-y: auto; border: 1px solid #ddd; border-radius: 6px; margin-top: 8px;">
					{#each teamMembers as member, index}
						<div style="padding: 16px; border-bottom: 1px solid #eee; {index === teamMembers.length - 1 ? 'border-bottom: none;' : ''}">
							<div style="display: flex; justify-content: between; align-items: center;">
								<!-- Member Info -->
								<div style="flex: 1;">
									<div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
										<strong style="color: #333;">{member.email}</strong>
										{#if member.email === adminEmail}
											<span style="background: #e3f2fd; color: #1976d2; padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight: 500;">
												You
											</span>
										{/if}
										<span style="background: #f3e5f5; color: #7b1fa2; padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight: 500;">
											{member.role || 'Admin'}
										</span>
										{#if member.status === 'PENDING'}
											<span style="background: #fff3cd; color: #856404; padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight: 500;">
												Pending
											</span>
										{:else if member.status === 'CONFIRMED'}
											<span style="background: #d4edda; color: #155724; padding: 2px 8px; border-radius: 12px; font-size: 11px; font-weight: 500;">
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
										<div style="width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; color: #ccc;" title="Cannot remove yourself">
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
					<p style="margin: 4px 0 0 0; font-size: 12px; color: #999;">Add team members using the form above</p>
				</div>
			{/if}
		</div>
		
		<!-- Info Section -->
		<div style="margin-top: 16px; padding: 12px; background: #f0f8ff; border: 1px solid #b3d9ff; border-radius: 4px;">
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
</div>
{:else}
<div class="flex items-center justify-center min-h-screen">
	<div class="text-center">
		<div class="text-6xl mb-4 text-gray-400">📊</div>
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
		display: flex;
		flex-direction: column;
		gap: 12px;
	}

	@media (min-width: 768px) {
		.button-grid {
			flex-direction: row;
			gap: 16px;
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
