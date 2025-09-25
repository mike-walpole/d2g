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
	<meta
		name="description"
		content="Privacy Policy for Dock2Gdansk - Professional Cargo Transportation Services"
	/>
</svelte:head>

<Header company="Dock2Gdansk" platformName={t('site_tagline', 'Professional Cargo Transportation')}>
	<HeaderNav>
		<HeaderNavItem href="/" text={t('nav.home', 'Home')} />
		<HeaderNavItem onclick={() => handleLanguageSwitch('en')} text={t('EN', 'EN')} />
		<HeaderNavItem onclick={() => handleLanguageSwitch('zh')} text={t('中文', '中文')} />
	</HeaderNav>
</Header>

<!-- Content Section -->
<section class="privacy-content">
	<div class="content-wrapper">
		<div class="content-container">
			<h1>PRIVACY POLICY</h1>

			<p class="date">Last Updated: September 2025</p>

			<h2>Quick Summary - What This Means for You</h2>
			<p>
				We help businesses find suppliers and vice versa. To do this, we collect personal information about business representatives (like names and contact details) and business requirements. We share relevant information between potential business partners to facilitate connections. You have full control over your data and can access, correct, or delete it at any time. We comply with privacy laws, including GDPR and PIPL, and we never sell your personal information.
			</p>
			<p>
				You may refer to the Terms of use for specific details of the services.
			</p>
			<p>
				Before you start using our services, please be sure to carefully read and understand the policy as follows, especially the terms marked in bold/bold underlined, and ensure that you fully understand and agree before starting to use them.
			</p>
			<p>
				Your agreement to the Dock2Gdansk platform Privacy Policy(Policy) indicates that you have understood the services we provide, as well as the necessary user information required for the operation of the corresponding service functions, and you have given the corresponding collection and use authorization.
			</p>
			<p>
				Given that our services are intended to help you or your company find business cooperation opportunities, we will share the information you provide with potential partners. Prior to sharing such information, we will obtain your separate consent to confirm your approval. However, it does not mean that you have separately agreed to enable extended business functions and process non-essential personal information.
			</p>
			<p>
				We will also separately seek your consent for the activation of relevant extended business functions, processing of non-essential personal information, and processing of sensitive personal information based on your actual usage.
			</p>

			<h3>Key Points:</h3>
			<p>
				We collect personal data of business contacts and company information to provide matching services<br/>
				We share relevant business information between potential partners to facilitate connections<br/>
				You can access, modify, or delete your data by contacting privacy@Dock2gdansk.com<br/>
				We respond to privacy requests within 30 days<br/>
				We comply with applicable privacy laws in your jurisdiction
			</p>

			<h2>Who We Are and How to Reach Us</h2>
			<p>
				Zarząd Morskiego Portu Gdańsk Spółka Akcyjna operates a B2B supplier matching platform ("Dock2Gdansk") connecting businesses with potential suppliers globally. We act as the data controller for personal information processed through our services.
			</p>

			<h3>Contact Us About Privacy:</h3>
			<p>
				Email: privacy@dock2gdansk.com<br/>
				Address: Gdansk, Poland<br/>
				Data Protection Officer: dpo@Dock2gdansk.com
			</p>
			<p>
				For users in China, our local representative can be reached at china-privacy@Dock2gdansk.com. EU users can also contact their local data protection authority with concerns.
			</p>

			<h2>Scope of Application</h2>
			<p>
				This Policy applies to all services provided by this platform to users in the European Union and the People's Republic of China via the website and new forms arising from technological developments. We and our affiliates have separate privacy policies or similar legal documents for the services they provide to you, and those services are governed by those privacy policies or similar legal documents.
			</p>
			<p>
				This Policy does not apply to services provided to you by other third parties. Other services are governed by their separately disclosed personal information collection and use rules. For example, if a third party offers you services based on Dock2Gdansk, please note that this Policy doesn't cover the information you share directly with them.
			</p>

			<h2>What Personal Information We Collect</h2>
			<p>
				When you use our services, we need to collect and use your personal information to fulfill the basic business functions required to provide our services to you. You must authorize us to collect and use the necessary information. Additionally, with your separate consent, we may share your personal information with potential business partners to facilitate communication and potential collaboration between you and them. If you refuse to provide the required information, you will be unable to use our services normally.
			</p>
			<p>
				When you submit a shipping inquiry to the platform, you will provide the following information: Company Name, Email Address, Phone Prefix, Phone Number, Cargo Type, "Inquiry Details" and "Where did you hear about us?"
			</p>
			<p>
				The phone number and email address you provide will serve as the primary communication channels for subsequent follow-ups, clarification of inquiries, and direct contact between local suppliers and international customers.
			</p>

			<h3>Business Information and Requirements</h3>
			<p>
				We collect detailed information about your business, including company name, e-mail address, phone number, and registration details, business address and industry type, detailed descriptions of products or services needed or offered, technical specifications and quality requirements, budget ranges and delivery timelines, and information about previous business relationships where relevant.
			</p>

			<h3>Automatic Information Collection</h3>
			<p>
				Our platform automatically collects certain information including your IP address and general location, device and browser information, how you navigate through our platform, when you log in and how long you stay, and system performance data to ensure our platform works properly.
			</p>

			<h2>Why and How We Use Your Information</h2>

			<h3>Primary Purpose: Matching Services</h3>
			<p>
				Our main purpose is to connect businesses with suitable partners. We analyze your requirements regarding our database of suppliers or buyers, present you with relevant matches based on your criteria, facilitate initial introductions between potential partners, and track whether matches lead to successful business relationships to improve our service.
			</p>
			<p>
				When sharing your information with potential partners, we will seek your separate consent through our website (link).
			</p>

			<h3>Platform Operations</h3>
			<p>
				We use your information to create and maintain your account, provide customer support when you need help, ensure our platform remains secure and prevent fraud, send important updates about our services, and comply with legal requirements like tax reporting.
			</p>

			<h3>Service Improvement</h3>
			<p>
				We analyze how our platform is used to make our matching algorithms more accurate, develop new features that users find valuable, understand market trends to provide better insights, and ensure our platform remains user-friendly and efficient.
			</p>

			<h2>Legal Basis for Processing Your Information</h2>
			<p>
				<strong>For EU Users (GDPR):</strong> We process your personal information because it's necessary to provide our matching services (contract performance), we have legitimate business interests in improving our platform and preventing fraud, you've given us consent for marketing communications, or we need to comply with legal obligations.
			</p>
			<p>
				<strong>For China Users (PIPL):</strong> We collect and use your personal information based on the following:
			</p>
			<p>
				If the information you provide contains personal information of other users, before providing such personal information to Dock2Gdansk, you must ensure that you have obtained legal authorization.
			</p>
			<p>
				B. If we use the information for purposes not specified in this Policy or use the information collected for a specific purpose for other purposes, we will obtain your consent in advance.
			</p>
			<p>
				C. In accordance with laws and regulations, we may collect and use your personal information without obtaining your consent in the following circumstances:
			</p>
			<p>
				I. It is necessary for the conclusion and performance of a contract in which an individual is a party;<br/>
				II. It is necessary to perform legal duties or obligations;<br/>
				III. In response to public health emergencies or in emergency situations where it is necessary to protect the life, health and property safety of natural persons;<br/>
				IV. Process personal information that individuals have voluntarily disclosed or that has been lawfully disclosed by others within a reasonable scope in accordance with the provisions of the PIPL;<br/>
				V. Other circumstances as prescribed by laws and administrative regulations.
			</p>
			<p>
				<strong>For Users in Other Jurisdictions:</strong> We comply with applicable local privacy laws and will process your information fairly and lawfully according to the requirements in your location.
			</p>

			<h2>When and Why We Share Your Information</h2>
			<p>
				We do not share your personal information with any company, organization, or individual other than the service provider of the Dock2Gdansk platform, except in the following circumstances
			</p>

			<h3>Legal Requirements</h3>
			<p>
				We may share your personal information with third parties as required by laws and regulations, for the resolution of litigation disputes, or in response to requests made by administrative or judicial authorities in accordance with the law.
			</p>
			<p>
				We may share information when required by law, court orders, or government requests, to protect our rights and property or the safety of our users, to prevent fraud or other illegal activities, or to enforce our terms of service. We will notify you of such sharing where legally permitted.
			</p>

			<h3>With Explicit Consent</h3>
			<p>
				<strong>Sharing with affiliated companies</strong> to facilitate our joint provision of services to you based on associated accounts, we will provide services to you based on the Dock2Gdansk account, identify abnormal accounts, and protect the personal and property safety of Dock2Gdansk affiliated companies, other users, or the public from being infringed upon. Your personal information may be shared with our affiliated companies and/or the service providers designated by them. We will only share necessary personal information and be bound by the purposes stated in this policy. If we share your sensitive personal information or if an affiliated company changes the purpose for which we use and process your personal information, we will seek your authorization and consent again.
			</p>
			<p>
				<strong>Sharing your personal information with other parties only after obtaining your separate consent:</strong> The core of our service involves sharing relevant information between potential business partners. When we identify a good match, we share business contact information, relevant product or service specifications, general company information, and location details necessary for initial business discussions. We only share what's necessary for the potential business relationship.
			</p>
			<p>
				We may provide aggregated or anonymous data to third parties; however, in such cases, we share non-personal information that cannot be used to identify you personally.
			</p>
			<p>
				We share your professional contact details and profile information with other businesses and suppliers on our platform. This is necessary to allow them to contact you, review your business profile, and initiate potential business relationships. This is the primary purpose of our service.
			</p>
			<p>
				By creating your profile and marking it as public, you provide us with your explicit consent to share your professional details (name, company, email, phone number) with other users of the platform for business matchmaking purposes.
			</p>
			<p>
				Please note that the information you voluntarily share or even publicly disclose when using our services may involve your or others' personal information, or even sensitive personal information. Please consider and make a decision more carefully.
			</p>
			<p>
				We may share your data with third-party vendors and service providers who help us operate our platform. This includes providers of hosting, analytics, IT support, and payment processing. These third parties are contractually obligated to process your data only on our behalf and to ensure its confidentiality and security.
			</p>
			<p>
				We will ask for your explicit consent to share your data with these third parties when you first register on our platform.
			</p>
			<p>
				You have the right to withdraw your consent at any time. You can do this sending a request to us at privacy@Dock2gdansk.com to have your account and data deleted.
			</p>

			<h3>Service Providers Who Help Us Operate</h3>
			<p>
				We work with trusted companies that help us provide our services, including cloud hosting providers like AWS for data storage, customer support platforms for help desk services, analytics tools for understanding platform usage, and security services for fraud prevention and platform protection. These providers can only use your information for the specific services they provide to us.
			</p>
			<p>
				We entrust your information to be processed for the legitimate, proper, necessary, specific, and clear purposes stated in this Policy. We authorize our partners to have access to the information necessary for them to perform their duties, and we require them, through agreements, not to use this information for any other purposes beyond the scope of the entrustment. If you authorize a partner to use your information for purposes not entrusted by us, they will obtain your separate consent.
			</p>

			<h3>Transfer</h3>
			<p>
				If we need to transfer your personal information due to reasons such as a merger, division, dissolution, or being declared bankrupt, we will inform you of the name or surname and contact details of the recipient. The recipient will continue to fulfill this policy and other legal obligations. If the recipient changes the original processing purpose or method, they will obtain your consent again.
			</p>

			<h3>Public Disclosure</h3>
			<p>
				Dock2Gdansk platform attaches great importance to protecting your personal information. We do not disclose it to irrelevant third parties, nor will we publicly disclose your personal information, except in the following circumstances
			</p>
			<p>
				Based on your active choice and other separate consents, we may publicly disclose your personal information.
			</p>
			<p>
				In cases where it is necessary to provide your personal information in accordance with the requirements of laws and regulations, mandatory administrative law enforcement, or judicial requirements, we may publicly disclose your personal information in the required type and manner of disclosure.
			</p>
			<p>
				If we determine that you have violated laws and regulations or seriously breached the relevant agreements and rules of Dock2Gdansk platform, or to protect the personal and property safety of Dock2Gdansk platform users or the public from being infringed upon, we may disclose your personal information, including the relevant violations and the measures that Dock2Gdansk platform has taken against you.
			</p>

			<h2>International Data Transfers</h2>

			<h3>How We Protect Your Data Across Borders</h3>
			<p>
				Our global platform may require transferring your information across international borders. We ensure these transfers are protected through European Commission-approved Standard Contractual Clauses for EU data, adequacy decisions where available, appropriate safeguards and contracts with all recipients, and compliance with local requirements, including PIPL for China-based data.
			</p>

			<h3>Special Protections for Sensitive Jurisdictions</h3>
			<p>
				For data from the EU, we ensure all recipients provide adequate protection equivalent to GDPR standards. For data from China, we conduct impact assessments for cross-border transfers and comply with PIPL requirements, including your separate consent and government approvals where necessary.
			</p>

			<h2>How Long We Keep Your Information</h2>
			<p>
				We keep your information only as long as necessary for our services and legal requirements. Active account information is maintained while your account is open, plus a reasonable time for service provision. Business requests and matching data are typically kept for 5 years to support ongoing business relationships and ensure legal compliance. Communication records are maintained for a period of 2 years for customer service purposes. Technical logs and analytics data are kept for 12 months for security and improvement purposes.
			</p>
			<p>
				You can request deletion of your information at any time, though some information may need to be retained for legal compliance or legitimate business purposes like contract fulfillment.
			</p>

			<h2>Your Privacy Rights and How to Use Them</h2>

			<h3>Rights Available to All Users</h3>
			<p>
				Regardless of your location, you can access the personal information we hold about you, request corrections to inaccurate information, ask us to delete your information in appropriate circumstances, object to how we use your information, and request we stop sending marketing communications.
			</p>

			<h3>Additional Rights for EU Users (GDPR)</h3>
			<p>
				EU users also have the right to restrict processing in certain situations, receive their data in a portable format, object to automated decision-making, and lodge complaints with their local data protection authority.
			</p>

			<h3>Additional Rights for China Users (PIPL)</h3>
			<p>
				China users have the right to know how their information is processed, delete personal information subject to legal exceptions, withdraw consent where applicable, and file complaints with Chinese regulatory authorities.
			</p>

			<h3>How to Exercise Your Rights</h3>
			<p>
				Email us at privacy@dock2gdansk.com with your request. We'll respond within 30 days (or sooner as required by local law). Please provide sufficient information to verify your identity and clearly specify what you're requesting. There's no charge for most requests, though we may charge a reasonable fee for excessive or repetitive requests.
			</p>

			<h2>Keeping Your Information Secure</h2>
			<p>
				We protect your information through encryption of data both when stored and transmitted, regular security testing and vulnerability assessments, strict access controls so only authorized personnel can access your data, employee training on data protection and security, and incident response plans to address any security issues quickly.
			</p>
			<p>
				If we experience a data breach that could affect you, we'll notify you and relevant authorities as required by law, typically within 72 hours of discovery. We extensively use AWS infrastructure, and are notified of any data breaches by email.
			</p>

			<h2>Updates to This Policy</h2>
			<p>
				To provide you with a better product and service experience, we are constantly striving to improve our products, services, and technologies. When there are new services or changes to business processes, we may update our privacy policy to inform you of the specific changes. However, without your explicit consent, we will not restrict the rights you enjoy under this policy.
			</p>
			<p>
				For major changes, we will also provide more prominent notifications (including through public announcements on Dock2Gdansk platform or by offering you pop-up prompts).
			</p>
			<p>
				The major changes referred to in this policy include, but are not limited to:
			</p>
			<p>
				The business model of the service has undergone significant changes. Such as the purpose of processing personal information, the types of personal information processed, and the way personal information is used;<br/>
				Changes in the privacy policy subject due to business adjustments, transactions or mergers and acquisitions, and the new subject recipient changes the original processing purpose and processing method;<br/>
				The main objects of personal information sharing or public disclosure have changed;<br/>
				There are significant changes in users' rights to personal information and the ways to exercise them;<br/>
				When the contact information of the person in charge of personal information protection and the complaint channels change;<br/>
				When the personal information protection impact assessment report indicates that the product has a significant impact on an individual's rights and interests.
			</p>
			<p>
				We will also archive previous versions of this policy on a dedicated page on Dock2Gdansk platform for your reference.
			</p>

			<h2>Children's Privacy</h2>
			<p>
				Our platform is exclusively for business use and is not intended for anyone under 18 years of age. We don't knowingly collect information from minors. If we discover we've collected such information, we'll delete it immediately. Meanwhile, if a minor provides us with personal information without the consent of his or her parents or guardians, the parents or guardians should contact dpo@Dock2gdansk.com to delete such personal information
			</p>

			<h2>Specific Jurisdictional Information</h2>
			<p>
				We comply with applicable privacy laws in all jurisdictions where we operate. If you're in a location not specifically mentioned, contact us at privacy@dock2gdansk.com for information about your local privacy rights.
			</p>

			<h2>Questions or Concerns</h2>
			<p>
				For any privacy questions or to exercise your rights, contact privacy@dock2gdansk.com. We're committed to addressing your concerns promptly and transparently.
			</p>
			<p>
				Data Protection Officer: dpo@Dock2gdansk.com<br/>
				China Representative: china-privacy@Dock2gdansk.com<br/>
				General Inquiries: info@Dock2gdansk.com
			</p>
			<p>
				If you're not satisfied with our response, you can contact your local data protection authority or privacy regulator.
			</p>

			<p style="margin-top: 40px;">
				I agree to the Terms of Use and Privacy Policy.<br/>
				I explicitly consent to the sharing of my professional profile and contact information with other users of the platform for business matchmaking.<br/>
				I explicitly consent to the sharing of my data with third-party service providers (such as hosting and analytics companies) as described in the Privacy Policy.
			</p>
		</div>
	</div>
</section>

<style>
	.privacy-content {
		padding: 64px 0;
		background: #ffffff;
		margin-top: 48px;
	}

	.content-wrapper {
		max-width: 900px;
		margin: 0 auto;
		padding: 0 16px;
	}

	.content-container {
		line-height: 1.6;
		color: #333;
		font-size: 16px;
	}

	h1 {
		font-size: 32px;
		margin-bottom: 16px;
		color: #000;
	}

	h2 {
		font-size: 24px;
		margin-top: 32px;
		margin-bottom: 16px;
		color: #000;
	}

	h3 {
		font-size: 20px;
		margin-top: 24px;
		margin-bottom: 12px;
		color: #000;
	}

	p {
		margin-bottom: 16px;
	}

	.date {
		font-style: italic;
		color: #666;
		margin-bottom: 32px;
	}

	/* Mobile responsive adjustments */
	@media (max-width: 768px) {
		.privacy-content {
			padding: 32px 0;
		}

		.content-wrapper {
			padding: 0 16px;
		}

		h1 {
			font-size: 28px;
		}

		h2 {
			font-size: 20px;
		}

		h3 {
			font-size: 18px;
		}
	}

	/* Match main layout header styles */
	:global(.bx--header) {
		position: fixed !important;
		top: 0 !important;
		z-index: 1000 !important;
	}
</style>