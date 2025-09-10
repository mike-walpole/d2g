<script>
	import { Button, Header, HeaderNav, HeaderNavItem } from 'carbon-components-svelte';
	import { t, currentLanguage, switchLanguage } from '$lib/stores/config.js';
	import { goto } from '$app/navigation';
	
	// Enhanced language switching with override tracking
	function handleLanguageSwitch(lang) {
		console.log('🔄 User manually switched to language:', lang);
		switchLanguage(lang);
		// Mark that user has manually chosen a language (override geolocation)
		localStorage.setItem('language-override', 'true');
		localStorage.setItem('preferred-language', lang);
	}
</script>

<svelte:head>
	<title>Privacy Policy - Dock2Gdansk</title>
	<meta name="description" content="Privacy Policy for Dock2Gdansk - Professional Cargo Transportation Services" />
</svelte:head>

<Header company="Dock2Gdansk" platformName={t('site_tagline', 'Professional Cargo Transportation')}>
	<HeaderNav>
		<HeaderNavItem href="/" text={t('nav.home', 'Home')} />
		<HeaderNavItem onclick={() => handleLanguageSwitch('en')} text={t('EN', 'EN')} />
		<HeaderNavItem onclick={() => handleLanguageSwitch('zh')} text={t('中文', '中文')} />
	</HeaderNav>
</Header>

<!-- Hero Section -->
<section style="background: #0043ce; color: white; padding: 120px 0 64px 0; margin-top: 48px;">
	<div style="max-width: 1200px; margin: 0 auto; padding: 0 16px; text-align: center;">
		<h1 style="font-size: 48px; font-weight: normal; margin-bottom: 16px; line-height: 1.2;">
			Privacy Policy
		</h1>
		<p style="font-size: 20px; margin-bottom: 32px; max-width: 800px; margin-left: auto; margin-right: auto;">
			Your privacy is important to us. Learn how we collect, use, and protect your information.
		</p>
		<p style="font-size: 16px; color: #b3d4fc;">
			<strong>Last Updated:</strong> August 2025
		</p>
	</div>
</section>

<!-- Content Section -->
<section class="privacy-content">
	<div class="content-wrapper">
		<div class="content-container">
			
			<!-- Quick Summary -->
			<div class="summary-box">
				<h2>Quick Summary - What This Means for You</h2>
				<p>
					We help businesses find suppliers and vice versa. To do this, we collect personal information about business representatives (like names and contact details) and business requirements. We share relevant information between potential business partners to facilitate connections. You have full control over your data and can access, correct, or delete it at any time. We comply with privacy laws including GDPR and PIPL, and we never sell your personal information.
				</p>
				
				<div class="key-points">
					<h3>Key Points:</h3>
					<ul>
						<li>We collect personal data of business contacts and company information to provide matching services</li>
						<li>We share relevant business information between potential partners to facilitate connections</li>
						<li>You can access, modify, or delete your data by contacting privacy@dock2gdansk.com</li>
						<li>We respond to privacy requests within 30 days</li>
						<li>We comply with applicable privacy laws in your jurisdiction</li>
					</ul>
				</div>
			</div>

			<!-- Section 1 -->
			<div class="section">
				<h2>1. Who We Are and How to Reach Us</h2>
				<p>
					Dock2Gdansk operates a B2B supplier matching platform connecting businesses with potential suppliers globally. We act as the data controller for personal information processed through our services.
				</p>
				
				<div class="contact-info">
					<h3>Contact Us About Privacy:</h3>
					<ul>
						<li><strong>Email:</strong> privacy@dock2gdansk.com</li>
						<li><strong>Address:</strong> Gdansk, Poland</li>
						<li><strong>Data Protection Officer:</strong> dpo@dock2gdansk.com</li>
					</ul>
					<p>
						For users in China, our local representative can be reached at china-privacy@dock2gdansk.com. EU users can also contact their local data protection authority with concerns.
					</p>
				</div>
			</div>

			<!-- Section 2 -->
			<div class="section">
				<h2>2. What Personal Information We Collect</h2>
				
				<div class="subsection">
					<h3>Information About Business Representatives</h3>
					<p>
						We collect personal information about individuals who represent businesses on our platform. This includes names, job titles, business email addresses, phone numbers, and sometimes personal contact information when provided. Even though this is collected in a business context, this remains personal data protected under privacy laws.
					</p>
				</div>

				<div class="subsection">
					<h3>Business Information and Requirements</h3>
					<p>
						We collect detailed information about your business including company name and registration details, business address and industry type, detailed descriptions of products or services needed or offered, technical specifications and quality requirements, budget ranges and delivery timelines, and information about previous business relationships where relevant.
					</p>
				</div>

				<div class="subsection">
					<h3>Platform Usage and Communications</h3>
					<p>
						We maintain records of how you use our platform, including search queries and preferences, messages sent through our system, interactions with potential matches, customer support conversations, and feedback you provide about our services.
					</p>
				</div>

				<div class="subsection">
					<h3>Automatic Information Collection</h3>
					<p>
						Our platform automatically collects certain information including your IP address and general location, device and browser information, how you navigate through our platform, when you log in and how long you stay, and system performance data to ensure our platform works properly.
					</p>
				</div>
			</div>

			<!-- Section 3 -->
			<div class="section">
				<h2>3. Why and How We Use Your Information</h2>
				
				<div class="subsection">
					<h3>Primary Purpose: Matching Services</h3>
					<p>
						Our main purpose is connecting businesses with suitable partners. We analyze your requirements against our database of suppliers or buyers, present you with relevant matches based on your criteria, facilitate initial introductions between potential partners, and track whether matches lead to successful business relationships to improve our service.
					</p>
				</div>

				<div class="subsection">
					<h3>Platform Operations</h3>
					<p>
						We use your information to create and maintain your account, provide customer support when you need help, ensure our platform remains secure and prevent fraud, send important updates about our services, and comply with legal requirements like tax reporting.
					</p>
				</div>

				<div class="subsection">
					<h3>Service Improvement</h3>
					<p>
						We analyze how our platform is used to make our matching algorithms more accurate, develop new features that users find valuable, understand market trends to provide better insights, and ensure our platform remains user-friendly and efficient.
					</p>
				</div>
			</div>

			<!-- Section 4 -->
			<div class="section">
				<h2>4. Legal Basis for Processing Your Information</h2>
				
				<div class="legal-basis">
					<p><strong>For EU Users (GDPR):</strong> We process your personal information because it's necessary to provide our matching services (contract performance), we have legitimate business interests in improving our platform and preventing fraud, you've given us consent for marketing communications, or we need to comply with legal obligations.</p>
					
					<p><strong>For China Users (PIPL):</strong> We process personal information with your consent where required, based on contract necessity for our services, for legitimate business interests while ensuring your rights are protected, or to meet legal and regulatory requirements.</p>
					
					<p><strong>For Users in Other Jurisdictions:</strong> We comply with applicable local privacy laws and will process your information fairly and lawfully according to the requirements in your location.</p>
				</div>
			</div>

			<!-- Section 5 -->
			<div class="section">
				<h2>5. When and Why We Share Your Information</h2>
				
				<div class="subsection">
					<h3>Facilitating Business Connections</h3>
					<p>
						The core of our service involves sharing relevant information between potential business partners. When we identify a good match, we share business contact information, relevant product or service specifications, general company information, and location details necessary for initial business discussions. We only share what's necessary for the potential business relationship.
					</p>
				</div>

				<div class="subsection">
					<h3>Service Providers Who Help Us Operate</h3>
					<p>
						We work with trusted companies that help us provide our services including cloud hosting providers like AWS for data storage, customer support platforms for help desk services, analytics tools for understanding platform usage, and security services for fraud prevention and platform protection. These providers can only use your information for the specific services they provide to us.
					</p>
				</div>

				<div class="subsection">
					<h3>Legal Requirements</h3>
					<p>
						We may share information when required by law, court orders, or government requests, to protect our rights and property or the safety of our users, to prevent fraud or other illegal activities, or to enforce our terms of service. We will notify you of such sharing where legally permitted.
					</p>
				</div>
			</div>

			<!-- Section 6 -->
			<div class="section">
				<h2>6. International Data Transfers</h2>
				
				<div class="subsection">
					<h3>How We Protect Your Data Across Borders</h3>
					<p>
						Our global platform may require transferring your information across international borders. We ensure these transfers are protected through European Commission-approved Standard Contractual Clauses for EU data, adequacy decisions where available, appropriate safeguards and contracts with all recipients, and compliance with local requirements including PIPL for China-based data.
					</p>
				</div>

				<div class="subsection">
					<h3>Special Protections for Sensitive Jurisdictions</h3>
					<p>
						For data from the EU, we ensure all recipients provide adequate protection equivalent to GDPR standards. For data from China, we conduct impact assessments for cross-border transfers and comply with PIPL requirements including government approvals where necessary.
					</p>
				</div>
			</div>

			<!-- Section 7 -->
			<div class="section">
				<h2>7. How Long We Keep Your Information</h2>
				<p>
					We keep your information only as long as necessary for our services and legal requirements. Active account information is maintained while your account is open plus reasonable time for service provision. Business request and matching data is typically kept for 5 years to support ongoing business relationships and legal compliance. Communication records are maintained for 2 years for customer service purposes. Technical logs and analytics data are kept for 12 months for security and improvement purposes.
				</p>
				<p>
					You can request deletion of your information at any time, though some information may need to be retained for legal compliance or legitimate business purposes like contract fulfillment.
				</p>
			</div>

			<!-- Section 8 -->
			<div class="section">
				<h2>8. Your Privacy Rights and How to Use Them</h2>
				
				<div class="subsection">
					<h3>Rights Available to All Users</h3>
					<p>
						Regardless of your location, you can access the personal information we hold about you, request corrections to inaccurate information, ask us to delete your information in appropriate circumstances, object to how we use your information, and request we stop sending marketing communications.
					</p>
				</div>

				<div class="subsection">
					<h3>Additional Rights for EU Users (GDPR)</h3>
					<p>
						EU users also have the right to restrict processing in certain situations, receive their data in a portable format, object to automated decision-making, and lodge complaints with their local data protection authority.
					</p>
				</div>

				<div class="subsection">
					<h3>Additional Rights for China Users (PIPL)</h3>
					<p>
						China users have the right to know how their information is processed, delete personal information subject to legal exceptions, withdraw consent where applicable, and file complaints with Chinese regulatory authorities.
					</p>
				</div>

				<div class="subsection">
					<h3>How to Exercise Your Rights</h3>
					<p>
						Email us at privacy@dock2gdansk.com with your request. We'll respond within 30 days (or sooner as required by local law). Please include enough information to verify your identity and specify exactly what you're requesting. There's no charge for most requests, though we may charge a reasonable fee for excessive or repetitive requests.
					</p>
				</div>
			</div>

			<!-- Section 9 -->
			<div class="section">
				<h2>9. Keeping Your Information Secure</h2>
				<p>
					We protect your information through encryption of data both when stored and transmitted, regular security testing and vulnerability assessments, strict access controls so only authorized personnel can access your data, employee training on data protection and security, and incident response plans to address any security issues quickly.
				</p>
				<p>
					If we experience a data breach that could affect you, we'll notify you and relevant authorities as required by law, typically within 72 hours of discovery.
				</p>
			</div>

			<!-- Section 10 -->
			<div class="section">
				<h2>10. Cookies and Website Analytics</h2>
				
				<div class="subsection">
					<h3>What We Use and Why</h3>
					<p>
						Our platform uses essential cookies necessary for basic functionality that cannot be disabled, analytics cookies to understand how users interact with our platform, and functional cookies to remember your preferences and settings. We only use marketing cookies with your explicit consent where required by law.
					</p>
				</div>

				<div class="subsection">
					<h3>Managing Cookie Preferences</h3>
					<p>
						You can manage cookie settings through your browser settings. Note that disabling essential cookies may affect platform functionality. We respect Do Not Track signals where technically feasible.
					</p>
				</div>
			</div>

			<!-- Section 11 -->
			<div class="section">
				<h2>11. Updates to This Policy</h2>
				<p>
					We may update this policy to reflect changes in our practices, new features, or legal requirements. We'll notify you of significant changes through email or prominent platform notices at least 30 days before changes take effect. Continued use of our services after notification means you accept the updated policy.
				</p>
			</div>

			<!-- Section 12 -->
			<div class="section">
				<h2>12. Children's Privacy</h2>
				<p>
					Our platform is exclusively for business use and not intended for anyone under 18. We don't knowingly collect information from minors. If we discover we've collected such information, we'll delete it immediately.
				</p>
			</div>

			<!-- Section 13 -->
			<div class="section">
				<h2>13. Specific Jurisdictional Information</h2>
				
				<div class="subsection">
					<h3>California Users (CCPA/CPRA)</h3>
					<p>
						California residents have additional rights including the right to know what personal information we collect and how it's used, delete personal information subject to exceptions, opt out of sale of personal information (we don't sell personal information), and non-discrimination for exercising privacy rights.
					</p>
				</div>

				<div class="subsection">
					<h3>Other Jurisdictions</h3>
					<p>
						We comply with applicable privacy laws in all jurisdictions where we operate. If you're in a location not specifically mentioned, contact us at privacy@dock2gdansk.com for information about your local privacy rights.
					</p>
				</div>
			</div>

			<!-- Section 14 -->
			<div class="section">
				<h2>14. Questions or Concerns</h2>
				<p>
					For any privacy questions or to exercise your rights, contact privacy@dock2gdansk.com. We're committed to addressing your concerns promptly and transparently.
				</p>
				
				<div class="contact-info">
					<p><strong>Data Protection Officer:</strong> dpo@dock2gdansk.com</p>
					<p><strong>China Representative:</strong> china-privacy@dock2gdansk.com</p>
					<p><strong>General Inquiries:</strong> info@dock2gdansk.com</p>
				</div>
				
				<p>
					If you're not satisfied with our response, you can contact your local data protection authority or privacy regulator.
				</p>
			</div>

			<!-- Back to Home Button -->
			<div class="back-button">
				<Button kind="primary" on:click={() => goto('/')}>
					← Back to Homepage
				</Button>
			</div>

		</div>
	</div>
</section>

<style>
	.privacy-content {
		padding: 64px 0;
		background: #f4f4f4;
		min-height: calc(100vh - 200px);
	}

	.content-wrapper {
		max-width: 900px;
		margin: 0 auto;
		padding: 0 16px;
	}

	.content-container {
		background: white;
		border-radius: 8px;
		box-shadow: 0 2px 8px rgba(0,0,0,0.1);
		padding: 48px;
		line-height: 1.6;
	}

	.summary-box {
		background: #f8f9fa;
		border-left: 4px solid #0043ce;
		padding: 24px;
		margin-bottom: 32px;
		border-radius: 4px;
	}

	.summary-box h2 {
		color: #0043ce;
		margin-top: 0;
		margin-bottom: 16px;
		font-size: 24px;
	}

	.key-points {
		margin-top: 20px;
	}

	.key-points h3 {
		color: #333;
		margin-bottom: 12px;
		font-size: 18px;
	}

	.key-points ul {
		margin: 0;
		padding-left: 20px;
	}

	.key-points li {
		margin-bottom: 8px;
		color: #555;
	}

	.section {
		margin-bottom: 40px;
		padding-bottom: 32px;
		border-bottom: 1px solid #e0e0e0;
	}

	.section:last-of-type {
		border-bottom: none;
	}

	.section h2 {
		color: #0043ce;
		font-size: 28px;
		margin-bottom: 20px;
		font-weight: 600;
	}

	.subsection {
		margin-bottom: 24px;
	}

	.subsection h3 {
		color: #333;
		font-size: 20px;
		margin-bottom: 12px;
		font-weight: 600;
	}

	.section p {
		color: #555;
		margin-bottom: 16px;
		font-size: 16px;
	}

	.contact-info {
		background: #f8f9fa;
		padding: 20px;
		border-radius: 4px;
		margin: 16px 0;
	}

	.contact-info h3 {
		color: #0043ce;
		margin-top: 0;
		margin-bottom: 12px;
	}

	.contact-info ul {
		margin: 0;
		padding-left: 20px;
	}

	.contact-info li {
		margin-bottom: 8px;
		color: #555;
	}

	.legal-basis p {
		margin-bottom: 16px;
		padding: 12px;
		background: #f8f9fa;
		border-radius: 4px;
		border-left: 3px solid #0043ce;
	}

	.back-button {
		text-align: center;
		margin-top: 48px;
		padding-top: 32px;
		border-top: 1px solid #e0e0e0;
	}

	/* Mobile responsive adjustments */
	@media (max-width: 768px) {
		.privacy-content {
			padding: 32px 0;
		}

		.content-wrapper {
			padding: 0 8px;
		}

		.content-container {
			padding: 24px 16px;
			border-radius: 4px;
		}

		.section h2 {
			font-size: 24px;
		}

		.subsection h3 {
			font-size: 18px;
		}

		.summary-box {
			padding: 16px;
		}

		.summary-box h2 {
			font-size: 20px;
		}

		.contact-info {
			padding: 16px;
		}
	}

	/* Tablet adjustments */
	@media (max-width: 1024px) and (min-width: 769px) {
		.content-container {
			padding: 36px 24px;
		}
	}

/* Match main layout header styles */
:global(.bx--header) {
	position: fixed !important;
	top: 0 !important;
	z-index: 1000 !important;
}
</style>