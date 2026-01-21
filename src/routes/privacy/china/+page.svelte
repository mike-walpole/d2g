<script>
	import { Header, HeaderNav, HeaderNavItem } from 'carbon-components-svelte';
	import { t, currentLanguage, switchLanguage } from '$lib/stores/config.js';

	function handleLanguageSwitch(lang) {
		console.log('User manually switched to language:', lang);
		switchLanguage(lang);
		localStorage.setItem('language-override', 'true');
		localStorage.setItem('preferred-language', lang);
	}
</script>

<svelte:head>
	<title>Privacy Policy for China - Dock2Gdansk | 中华人民共和国境内用户隐私政策</title>
	<meta
		name="description"
		content="Dock2Gdansk Privacy Policy for Users in the People's Republic of China - 中华人民共和国境内用户隐私政策"
	/>
</svelte:head>

<Header company="Dock2Gdansk" platformName={t('site_tagline', 'Professional Cargo Transportation')}>
	<HeaderNav>
		<HeaderNavItem href="/" text={t('nav.home', 'Home')} />
		<HeaderNavItem onclick={() => handleLanguageSwitch('en')} text={t('EN', 'EN')} />
		<HeaderNavItem onclick={() => handleLanguageSwitch('zh')} text={t('中文', '中文')} />
	</HeaderNav>
</Header>

<section class="privacy-content">
	<div class="content-wrapper">
		<div class="content-container">
			<h1>Dock2Gdansk Privacy Policy for Users in the People's Republic of China</h1>
			<h1 class="chinese-title">Dock2Gdansk中华人民共和国境内用户隐私政策</h1>

			<p class="date">Last Updated: January 2026 / 最后更新：2026年1月</p>

			<!-- Attention Section -->
			<div class="bilingual-section attention-box">
				<p><strong>Attention:</strong> This Privacy Policy governs the services provided by Zarząd Morskiego Portu Gdańsk SA, address: Zamknięta street no. 18, Postal Code 80-545 Gdansk, NIP (Taxpayer Identification Number): 583-24-61-866, Registered in District Court Gdansk-Polnoc in Gdansk VII Commercial Division of the National Court Register No. KRS 0000040398. Share / paid up capital: PLN 2,109,250 ("we" or "us") through dock2gdansk.dagodigital.com ("Dock2Gdansk") exclusively to users located within the territory of the People's Republic of China. It does not apply to services provided by Dock2Gdansk to users outside the territory of the People's Republic of China via any digital platform. For the Privacy Policy applicable to users outside the PRC, please refer to the dedicated policy accessible <a href="/privacy?region=global">here</a>.</p>
				<p class="chinese"><strong>请注意：</strong>本政策适用于由Zarząd Morskiego Portu Gdańsk SA地址：波兰格但斯克（Gdańsk）Zamknięta街18号，邮政编码：80-545，税号（NIP）：583-24-61-866，注册于：格但斯克北区地方法院第七商事部国家法院注册处（KRS）编号 0000040398注册资本 / 实缴资本：2,109,250 波兰兹罗提（PLN）（以下简称"我们"）开发并向中华人民共和国境内用户以网站dock2gdansk.com（以下简称"Dock2Gdansk"）形态提供的各项服务。本政策不适用于Dock2Gdansk向中华人民共和国境内以外的用户以网站形态提供的各项产服务。中华人民共和国境内以外的用户的隐私政策请<a href="/privacy?region=global">点此查看</a>。</p>
			</div>

			<!-- Welcome Section -->
			<div class="bilingual-section">
				<p><strong>Welcome to our Services!</strong> We recognize the importance of your personal information to you, and your trust is of utmost importance to us. In compliance with applicable laws and regulations and guided by industry best practices, we are committed to providing robust protection for the security of your personal information. To this end, we have formulated the Dock2Gdansk Privacy Policy for Users in the People's Republic of China ("Privacy Policy" or "this Policy") to ensure you fully understand: How we collect, use, process, share, transfer, disclose, store, and protect your personal information during your use of Dock2Gdansk Services; and the rights and mechanisms available to you for managing your personal information. We encourage you to read this Policy in conjunction with our <a href="/terms/china">Terms of Use</a>.</p>
				<p class="chinese"><strong>欢迎您使用我们的服务！</strong>我们深知用户信息对您的重要性，您的信任对我们非常重要，我们将根据法律法规要求并参照行业最佳实践为您的用户信息安全提供充分保障。为此，我们制定本《Dock2Gdansk中华人民共和国境内用户隐私政策》（下称"本隐私政策"或"本政策"）以便您充分了解，在您使用Dock2Gdansk的服务的过程中，我们会如何收集、使用、委托处理、共享、转移、公开、存储和保护您的用户信息，以及您可以如何管理您的用户信息。请您结合Dock2Gdansk的<a href="/terms/china">《使用条款》</a>阅读本政策。</p>
			</div>

			<!-- EU Data Protection Notice -->
			<div class="bilingual-section">
				<p>Zarząd Morskiego Portu Gdańsk S.A. has headquarters in Poland (European Union), so your personal data shall be protected by EU laws. We are processing your data for the following purposes: Matching Services, current communication, providing other Platform Operations and Service Improvement. You shall have the right to obtain access to your data, to have it erased, to restrict its processing, receive your data in a portable format or to complain to a supervisory authority. You also have the right to rectification of your personal data. Detailed information on the processing of your personal data under EU laws can be found <a href="/privacy?region=global">here</a>.</p>
				<p class="chinese">Zarząd Morskiego Portu Gdańsk S.A. 的总部位于波兰（欧盟），因此您的个人数据将受到欧盟法律的保护。我们出于以下目的处理您的个人数据：提供撮合服务、进行日常沟通、开展其他平台运营以及改进服务。您有权访问您的个人数据、要求删除您的个人数据、限制对其处理、以可携带的格式接收您的数据，或者向监督机构提出投诉。您亦有权要求更正您的个人数据。关于依据欧盟法律处理您个人数据的详细信息，请<a href="/privacy?region=global">见此处</a>。</p>
			</div>

			<!-- Platform Description -->
			<div class="bilingual-section">
				<p>Dock2Gdansk is a business-to-business (B2B) platform (or "Platform") that connects and enables transactions between users and potential business partners for the buying and selling of services. We help businesses find suppliers and connect with them. To do this, we collect personal information about business representatives (like names and contact details) and business requirements. We share relevant information between potential business partners to facilitate connections. You have full control over your data and can access, correct, or delete it at any time. We comply with privacy laws, including GDPR and PIPL, and we never sell your personal information.</p>
				<p class="chinese">Dock2Gdansk是一个企业对企业（B2B）平台（或"平台"），其连接并促进用户和潜在商业伙伴之间的服务买卖。我们帮助企业寻找供应商，同时也为供应商提供商业对接服务。为此，我们会收集企业代表的个人信息（包括姓名、联系方式）及业务需求。通过在潜在合作伙伴之间共享相关信息，促进双方建立联系。您对个人数据拥有完全控制权，可随时访问、修改或删除信息。我们严格遵守《通用数据保护条例》（GDPR）、《个人信息保护法》（PIPL）等隐私法规，并承诺绝不出售您的个人信息。</p>
			</div>

			<!-- Important Notice -->
			<div class="bilingual-section highlight-box">
				<p><strong>Before you start using our services, please be sure to carefully read and understand the policy as follows, especially the terms marked in bold/bold underlined, and ensure that you fully understand and agree before starting to use them.</strong></p>
				<p class="chinese"><strong>在开始使用我们的服务之前，请务必仔细阅读并理解以下政策，特别是标有粗体/下划线的条款，并确保您在开始使用之前充分理解并同意。</strong></p>
			</div>

			<!-- Agreement Section -->
			<div class="bilingual-section">
				<p>Your agreement to this Policy indicates that you have fully understood the services we provide, as well as the necessary user information required for the operation of the corresponding service functions, and you have given the corresponding collection and use authorization.</p>
				<p class="chinese">您同意本政策即表示您已充分理解我们提供的服务以及运行相关服务功能所需的必要用户信息，并且您已授权我们收集和使用这些信息。</p>
			</div>

			<div class="bilingual-section">
				<p>Given that our services are intended to help you or your company find business cooperation opportunities, we will share the information you provide with potential partners. Prior to sharing such information, we will obtain your separate consent to confirm your approval. However, it does not mean that you have separately agreed to enable extended business functions and process non-essential personal information. We will also separately seek your consent for the activation of relevant extended business functions, processing of non-essential personal information, and processing of sensitive personal information based on your actual usage.</p>
				<p class="chinese">鉴于我们的服务旨在帮助您或您的公司寻找商业合作机会，我们将与潜在合作伙伴共享您提供的信息。在共享此类信息之前，我们将获得您的单独同意以确认您的批准。但是，这并不意味着您已单独同意启用扩展业务功能和处理非必要的个人信息。相关扩展业务功能的开启、处理非必要个人信息以及处理敏感个人信息，我们会根据您的实际使用情况单独征求您的同意。</p>
			</div>

			<!-- Table of Contents -->
			<div class="bilingual-section toc-section">
				<p><strong>This Privacy Policy assists you in understanding the following key aspects:</strong></p>
				<p class="chinese"><strong>本隐私政策可帮助您了解以下关键内容：</strong></p>
				<ul class="toc-list">
					<li>Scope of Applicability / 适用范围</li>
					<li>Collection and Use of Personal Information / 信息收集及使用</li>
					<li>Sharing, Entrusted Processing, Transfer, and Disclosure of Personal Information / 个人信息的共享、委托处理、转让、公开</li>
					<li>User Rights and How to Use Them / 用户权利及其行使</li>
					<li>Storage and Protection of Information / 信息的储存与保护</li>
					<li>Updates of This Policy / 政策更新</li>
					<li>Protection of Minors / 未成年人保护</li>
					<li>Contact Us / 联系我们</li>
					<li>Supplementary Provisions / 附则</li>
				</ul>
			</div>

			<!-- Section 1: Scope of Application -->
			<h2>Scope of Application / 适用范围</h2>
			<div class="bilingual-section">
				<p>This Policy applies to all services provided by this platform to users in the People's Republic of China via the website and any new forms that may arise from technological developments. We and our affiliates have separate privacy policies or similar legal documents for the services they provide to you, and those services are governed by those privacy policies or similar legal documents.</p>
				<p class="chinese">本政策适用于Dock2Gdansk向中华人民共和国境内用户以网站以形态提供的各项服务。我们及关联公司就其向您提供的服务单独设有隐私政策或类似法律文件，相应服务适用相应隐私政策或类似法律文件。</p>
			</div>

			<div class="bilingual-section">
				<p>This Policy does not apply to services provided to you by other third parties. Other services are governed by their separately disclosed rules regarding personal information collection and use. For example, if a third party provides you with services based on Dock2Gdansk, this Policy does not apply to the information you provide to the third party.</p>
				<p class="chinese">本政策不适用于其他第三方向您提供的服务，其他服务适用其向您另行说明的个人信息收集使用规则。例如，第三方基于Dock2Gdansk向您提供服务时，您向第三方提供的信息不适用本政策。</p>
			</div>

			<!-- Section 2: Collection and Use -->
			<h2>Collection and Use of Personal Information / 信息收集及使用</h2>
			<div class="bilingual-section">
				<p>When you use our services, we need to collect and use your personal information to fulfill the basic business functions required to provide our services to you. You must authorize us to collect and use the necessary information. Additionally, with your separate consent, we may share your personal information with potential business partners to facilitate communication and potential collaboration between you and them. If you refuse to provide the required information, you will be unable to use our services normally.</p>
				<p class="chinese">使用我们的服务时，我们需要收集并使用您的个人信息以满足提供服务所需的基本业务功能。您必须授权我们收集和使用必要信息。此外，经您同意后，我们可能会将您的个人信息与潜在商业伙伴共享，以便促进您与他们的沟通及潜在合作。如果您拒绝提供所需信息，则无法正常使用我们的服务。</p>
			</div>

			<h3>Core Services / 基础服务</h3>
			<div class="bilingual-section">
				<p>When you submit a shipping inquiry to the platform, you will provide the following information: Company Name, Email Address, Phone Prefix, Phone Number, Cargo Type, "Inquiry Details", and "Where did you hear about us?"</p>
				<p class="chinese">当您向平台提交运输询盘时，您将提供以下信息：公司名称、电子邮箱地址、电话前缀、电话号码、货物类型、"问询详情"和"您是从哪里听说我们的？"</p>
			</div>

			<div class="bilingual-section">
				<p>The phone number and email address you provide will serve as the primary communication channels for subsequent follow-ups, clarification of inquiries, and direct contact between local suppliers and international customers.</p>
				<p class="chinese">您提供的电话号码和电子邮箱地址将作为后续跟进、问询澄清以及本地供应商与国际客户直接联系的主要沟通渠道。</p>
			</div>

			<div class="bilingual-section">
				<p>We will send you potential business partner matching results via email. By doing so, we hereby separately request your separate consent to share your personal information (including your mobile phone number and email address) with such counterparties.</p>
				<p class="chinese">我们将通过电子邮件向您发送潜在商业合作伙伴匹配结果。通过发送电子邮件，我们另行请求您单独同意将您的个人信息（包括手机号码和电子邮箱地址）与该方共享。</p>
			</div>

			<div class="bilingual-section">
				<p>Our main purpose is to connect businesses with suitable partners. We analyze your requirements regarding our database of suppliers or customers, present you with relevant matches based on your criteria, facilitate initial introductions between potential partners, and track whether matches lead to successful business relationships to improve our service.</p>
				<p class="chinese">我们的主要目标是为企业与合适的合作伙伴建立联系。我们会分析您的需求，与我们的供应商或客户数据库进行比对，根据您的标准为您呈现相关匹配对象，促进潜在合作伙伴之间的初步接触，并跟踪这些匹配是否转化为成功的商业合作关系，从而提升我们的服务质量。</p>
			</div>

			<div class="bilingual-section">
				<p>We accept your exercise of rights regarding access, rectification, erasure, and modification of authorization for your submitted information via email.</p>
				<p class="chinese">我们接受您通过电子邮件行使访问、更正、删除和修改提交信息授权的权利。</p>
			</div>

			<h3>Automatic Information Collection / 自动收集的信息</h3>
			<div class="bilingual-section">
				<p>Our platform automatically collects certain information, including your IP address and general location, device and browser information, how you navigate through our platform, when you log in, and how long you stay, and system performance data to ensure our platform works properly.</p>
				<p class="chinese">我们的平台自动收集某些信息，包括您的IP地址和一般位置、设备和浏览器信息、您如何通过我们的平台导航、您登录的时间和您停留的时间，以及系统性能数据，以确保我们的平台正常工作。</p>
			</div>

			<h3>Platform Operations / 平台运作</h3>
			<div class="bilingual-section">
				<p>We use your information to provide and maintain access to the platform, provide customer support when you need it, ensure our platform remains secure and prevents fraud, send important updates about our services, and comply with legal requirements such as reporting required by law.</p>
				<p class="chinese">我们使用您的信息来创建和维护您的账户，在您需要帮助时提供客户支持，确保我们的平台保持安全并防止欺诈，发送有关我们服务的重要更新，并遵守法律要求，如依法报告。</p>
			</div>

			<h3>Service Improvement / 服务改进</h3>
			<div class="bilingual-section">
				<p>We analyze how our platform is used to refine our matching algorithms, develop new features that users find valuable, understand market trends to provide better insights, and ensure our platform remains user-friendly and efficient.</p>
				<p class="chinese">我们分析如何使用我们的平台来提高匹配算法的准确性，开发用户认为有价值的新功能，了解市场趋势以提供更好的见解，并确保我们的平台保持用户友好和高效。</p>
			</div>

			<h3>Other Regulations on the Collection and Use of Personal Information / 收集和使用个人信息的其他规则</h3>
			<div class="bilingual-section">
				<p>If the information you provide contains Personal Information of other individuals, you must ensure that you have obtained lawful authorization prior to providing such personal information to Dock2Gdansk.</p>
				<p class="chinese">若您提供的信息中含有其他用户的个人信息，在Dock2Gdansk提供这些个人信息之前，您需确保您已经取得合法的授权。</p>
			</div>

			<div class="bilingual-section">
				<p>If we use your personal information for purposes not expressly specified in this Policy or use personal information collected for a specific purpose for other purposes, we will obtain your separate consent in advance.</p>
				<p class="chinese">若我们将信息用于本政策未载明的其他用途，或者将基于特定目的收集而来的信息用于其他目的，均会事先获得您的单独同意。</p>
			</div>

			<div class="bilingual-section">
				<p>Under applicable laws and regulations, we may collect and use your personal information without obtaining your consent in the following circumstances:</p>
				<p class="chinese">根据法律法规，以下情形中我们收集和使用您的个人信息无需征得您的同意：</p>
				<ul>
					<li>Necessary for entering into, performing, or otherwise necessary for a contract to which the individual is a party;<br/>为订立、履行个人作为一方当事人的合同所必需，或者按照依法制定的劳动规章制度和依法签订的集体合同实施人力资源管理所必需；</li>
					<li>Necessary for fulfilling statutory duties or legal obligations;<br/>为履行法定职责或者法定义务所必需；</li>
					<li>Necessary for responding to public health emergencies or protecting the life, health, and property safety of natural persons in emergency situations;<br/>为应对突发公共卫生事件，或者紧急情况下为保护自然人的生命健康和财产安全所必需；</li>
					<li>Processing publicly disclosed personal information within reasonable scope as permitted under the Personal Information Protection Law (PIPL) or other legally disclosed personal information;<br/>依照《个人信息保护法》规定在合理的范围内处理个人自行公开或者其他已经合法公开的个人信息；</li>
					<li>Other circumstances as provided by laws or administrative regulations.<br/>法律、行政法规规定的其他情形。</li>
				</ul>
			</div>

			<!-- Section 3: Sharing, Transfer, Disclosure -->
			<h2>Sharing, Entrusted Processing, Transfer, and Disclosure of Personal Information / 个人信息的共享、委托处理、转让、公开</h2>

			<h3>When and Why We Share Your Information / 何时以及为何共享您的信息</h3>
			<div class="bilingual-section">
				<p>We do not share your personal information with any company, organization or individual other than the service provider of the Dock2Gdansk platform, except in the following circumstances:</p>
				<p class="chinese">我们不会与Dock2Gdansk平台的服务提供商以外的任何公司、组织或个人共享您的个人信息，以下情况除外：</p>
			</div>

			<h4>Legal Requirements / 法定情形</h4>
			<div class="bilingual-section">
				<p>We may share your personal information with third parties as required by laws and regulations, for the resolution of litigation disputes, or in response to requests made by administrative or judicial authorities in accordance with the law.</p>
				<p class="chinese">我们可能会根据法律法规的要求，与第三方共享您的个人信息，以解决诉讼纠纷，或响应行政或司法当局依法提出的请求。</p>
			</div>

			<div class="bilingual-section">
				<p>We may share information when required by law, court orders, or government requests, to protect our rights and property or the safety of our users, to prevent fraud or other illegal activities, or to enforce our terms of service. We will notify you of such sharing where legally permitted.</p>
				<p class="chinese">为保护我们的权利和财产或用户的安全、防止欺诈或其他非法活动或执行我们的服务条款，我们可能会在法律要求、法院命令或政府请求时共享信息。在法律允许的情况下，我们会通知您此类共享。</p>
			</div>

			<h4>With Explicit Consent / 通过明确的同意</h4>
			<div class="bilingual-section">
				<p><strong>Sharing with affiliated companies</strong> to facilitate our joint provision of services to you based on associated companies, we will provide services to you based on the Dock2Gdansk account, identify abnormal inquiries, and protect the personal and property safety of Dock2Gdansk affiliated companies, other users or the public from being infringed upon. Your personal information may be shared with our affiliated companies and/or the service providers designated by them. We will only share necessary personal information and be bound by the purposes stated in this policy. If we share your sensitive personal information or if an affiliated company changes the purpose of using and processing your personal information, we will seek your authorization and consent again.</p>
				<p class="chinese"><strong>与关联公司共享</strong>为便于与关联公司共同为您提供服务，我们将基于Dock2格但斯克账户为您提供服务，识别异常账户，并保护Dock2格但斯克关联公司、其他用户或公众的个人及财产安全不受侵害。您的个人信息可能会与我们的关联公司及其指定的服务提供商共享。我们仅会共享必要的个人信息，并严格遵守本政策所述目的。若涉及敏感个人信息共享，或关联公司变更使用处理您个人信息的目的时，我们将再次征求您的授权同意。</p>
			</div>

			<div class="bilingual-section">
				<p><strong>Sharing your personal information with other parties only after obtaining your separate consent:</strong> The core of our service involves sharing relevant information between potential business partners. When we identify a good match, we share business contact information, relevant product or service specifications, general company information, and location details necessary for initial business discussions. We only share what's necessary for the potential business relationship.</p>
				<p class="chinese"><strong>在获得您的单独授权后，才会与第三方共享个人信息：</strong>作为核心服务内容，我们致力于在潜在商业伙伴之间实现信息共享。当发现合适合作对象时，我们会提供必要的商务联系方式、产品或服务规格、企业概况及地理位置等关键信息，但仅限于建立初步商业合作所需的必要内容。</p>
			</div>

			<div class="bilingual-section">
				<p>We may provide aggregated or anonymous data to third parties, but in such cases, what we share is non-personal information that cannot identify you personally.</p>
				<p class="chinese">我们可能会向第三方提供汇总或匿名数据，但在此类情况下，我们共享的不是个人身份信息。</p>
			</div>

			<div class="bilingual-section">
				<p>You can view the data sharing situation description below of Dock2Gdansk platform:</p>
				<p class="chinese">您可查看以下Dock2Gdansk平台的数据共享情况说明：</p>
				<p>The partners or suppliers with whom we share data are as follows: comprehensive business warehousing and transport services in Gdańsk, specializing in efficient logistics solutions for both storage and transportation needs; a specialized transshipment and storage facility designed for handling agricultural and food products; large-scale transport, forwarding, customs, and terminal services, ensuring efficient logistics and smooth goods handling; port operating company providing services in cargo transshipment for international trade, between maritime and inland (ship, barge) and land transport (trucks, wagons).</p>
			</div>

			<div class="bilingual-section highlight-box">
				<p>Please note that the information you voluntarily share or even publicly disclose when using our services may involve your or others' personal information, or even sensitive personal information. Please consider and make a decision more carefully.</p>
				<p class="chinese">请注意，您在使用我们服务时自愿共享甚至公开分享的信息，可能会涉及您或他人的个人信息甚至敏感个人信息。请您更加谨慎地考虑并做出决定。</p>
			</div>

			<h3>When and Why We Entrust Third Parties to Process Your Information / 何时以及为何委托他人处理您的信息</h3>
			<div class="bilingual-section">
				<p>We work with trusted companies that help us provide our services including cloud hosting providers like AWS for data storage, customer support platforms for help desk services, analytics tools for understanding platform usage, and security services for fraud prevention and platform protection. These providers can only use your information for the specific services they provide to us.</p>
				<p class="chinese">我们与值得信赖的公司合作，这些公司帮助我们提供服务，包括用于数据存储的云托管提供商AWS、用于帮助台服务的客户支持平台、用于了解平台使用的分析工具以及用于欺诈预防和平台保护的安全服务。这些提供商只能将您的信息用于他们向我们提供的特定服务。</p>
			</div>

			<div class="bilingual-section">
				<p>We entrust your information to be processed for the legitimate, proper, necessary, specific and clear purposes stated in this Policy. We authorize our partners to have access to the information necessary for them to perform their duties, and we require them through agreements not to use this information for any other purposes beyond the scope of the entrustment. If you authorize a partner to use your information for purposes not entrusted by us, they will obtain your separate consent.</p>
				<p class="chinese">我们承诺，您的信息将仅用于本政策所述的合法、正当、必要、特定且明确之目的。我们授权合作伙伴获取履行职责所需的信息，并通过协议禁止其将信息用于委托范围之外的其他用途。若您授权合作伙伴使用非委托用途的信息，需另行获得您的书面同意。</p>
			</div>

			<h3>When and Why We Transfer Your Information / 何时以及为何转移您的信息</h3>
			<div class="bilingual-section">
				<p>If we need to transfer your personal information due to reasons such as merger, division, dissolution or being declared bankrupt, we will inform you of the name or surname and contact details of the recipient. The recipient will continue to fulfill this policy and other legal obligations. If the recipient changes the original processing purpose or method, they will obtain your consent again.</p>
				<p class="chinese">因合并、分立、解散或被宣告破产等原因需要向接收方转移个人信息的，我们会告知您接收方的名称或姓氏及联系方式。接收方将继续履行本政策及其他法律义务。接收方如变更原处理目的或方式，将再次征得您的同意。</p>
			</div>

			<h3>How We Protect Your Information Across Borders / 我们如何在数据跨境传输中保护您的信息</h3>
			<div class="bilingual-section">
				<p>Our global platform may require transferring your information across international borders. We ensure these transfers are protected through European Commission-approved Standard Contractual Clauses for EU data, adequacy decisions where available, appropriate safeguards and contracts with all recipients, and compliance with local requirements, including PIPL for China-based data.</p>
				<p class="chinese">我们的全球平台可能需要将您的信息传输到国际边界。我们通过欧盟委员会批准的欧盟数据标准合同条款、适用的充分性决定、适当的保障措施和与所有接收方签订的合同，以及遵守包括针对中国数据的PIPL在内的要求，来确保这些传输受到保护。</p>
			</div>

			<div class="bilingual-section">
				<p>For data from the EU, we ensure all recipients provide adequate protection equivalent to GDPR standards. For data from China, we conduct impact assessments for cross-border transfers and comply with PIPL requirements, including your separate consent and government approvals where necessary.</p>
				<p class="chinese">对于来自欧盟的数据，我们确保所有接收方提供与GDPR标准相当的充分保护。对于来自中国的数据，我们对跨境传输进行影响评估，并遵守PIPL要求，包括您的单独同意和必要的政府批准。</p>
			</div>

			<h3>When and Why We Publicly Disclose Your Information / 何时以及为何公开您的信息</h3>
			<div class="bilingual-section">
				<p>Dock2Gdansk platform attaches great importance to protecting your personal information. We do not disclose it to irrelevant third parties, nor will we publicly disclose your personal information, except in the following circumstances:</p>
				<p class="chinese">Dock2Gdansk平台非常重视保护您的个人信息。我们不会向无关的第三方披露您的个人信息，也不会公开披露您的个人信息，除非在以下情况下：</p>
				<ul>
					<li>Based on your active choice and other separate consents, we may publicly disclose your personal information.<br/>根据您的主动选择和其他单独的同意，我们可能会公开披露您的个人信息。</li>
					<li>In cases where it is necessary to provide your personal information in accordance with the requirements of laws and regulations, mandatory administrative law enforcement or judicial requirements, we may publicly disclose your personal information in the required type and manner of disclosure.<br/>根据法律法规要求、行政强制执行或者司法要求，需要提供个人信息的，我们可能会按照要求的方式公开您的个人信息。</li>
					<li>If we determine that you have violated laws and regulations or seriously breached the relevant agreements and rules of Dock2Gdansk platform, or to protect the personal and property safety of Dock2Gdansk platform users or the public from being infringed upon, we may disclose your personal information, including the relevant violations and the measures that Dock2Gdansk platform has taken against you.<br/>如果我们确定您有违反法律法规或严重违反Dock2Gdansk平台相关协议和规则，或者为保护Dock2Gdansk平台用户或公众的人身、财产安全免受侵害，我们可能会披露您的个人信息，包括相关的违规行为以及Dock2Gdansk平台针对您采取的措施。</li>
				</ul>
			</div>

			<!-- Section 4: User Rights -->
			<h2>User Rights and How to Use Them / 用户权利及其行使</h2>

			<h3>Rights Available to All Users / 所有用户均可获得的权利</h3>
			<div class="bilingual-section">
				<p>Regardless of your location, you can access the personal information we hold about you, request corrections to inaccurate information, ask us to delete your information in appropriate circumstances, object to how we use your information, and request we stop sending marketing communications.</p>
				<p class="chinese">无论您身在何处，您都可以访问我们持有的关于您的个人信息，要求更正不准确的信息，在适当的情况下要求我们删除您的信息，反对我们使用您的信息，并要求我们停止发送营销信息。</p>
			</div>

			<div class="bilingual-section">
				<p>China users have the right to know how their information is processed, delete personal information subject to legal exceptions, withdraw consent where applicable, and file complaints with Chinese regulatory authorities.</p>
				<p class="chinese">中国用户有权知道其信息如何被处理，删除受法律例外情况约束的个人信息，在适用情况下撤回同意，并向中国监管机构提出投诉。</p>
			</div>

			<h3>Protection of Personal Information of Deceased Users / 保护已故用户的个人信息</h3>
			<div class="bilingual-section">
				<p>We have formulated a personal information protection system for the deceased in accordance with the relevant provisions of PIPL. If a user of our services passes away, their close relatives may, for their own legitimate and proper interests, contact us through the methods specified in the "Contact Us" section of this policy to exercise the rights of accessing, copying, correcting, and deleting the relevant personal information of the deceased user, except where the deceased user had other arrangements during their lifetime.</p>
				<p class="chinese">我们根据《个人信息保护法》相关规定，为逝者制定了个人信息保护制度。若用户不幸离世，其直系亲属可依据本政策"联系我们"章节中指定的方式与我们联系，为维护自身合法权益，行使访问、复制、更正及删除逝者个人信息的权利。但若逝者生前另有安排，则不在此列。</p>
			</div>

			<div class="bilingual-section">
				<p>Please be informed: to fully protect the personal information rights and interests of the deceased user, the close relatives of the deceased user who apply to exercise the rights stipulated in this article need to submit the identity documents of the deceased user, the death certificate, the identity documents of the applicant, and the proof of the kinship between the applicant and the deceased user in accordance with the process designated by us or the prompts of the customer service, and provide the type and purpose of the rights to be exercised.</p>
				<p class="chinese">请您知悉：为充分保障已故用户个人信息权益，申请行使本条款所规定权利的已故用户近亲属需按照我方指定流程或客服提示提交已故用户身份证明、死亡证明、申请人身份证明及申请人与已故用户亲属关系证明，并说明拟行使权利的类型和目的。</p>
			</div>

			<h3>How to Exercise Your Rights / 如何行使您的权利</h3>
			<div class="bilingual-section">
				<p>Email us at <a href="mailto:info@dock2gdansk.com">info@dock2gdansk.com</a> with your request. We'll respond within 15 days (or sooner as required by local law). Please include enough information to verify your identity and specify exactly what you're requesting.</p>
				<p class="chinese">请将您的请求发送至<a href="mailto:info@dock2gdansk.com">info@dock2gdansk.com</a>邮箱。我们将在15天内回复（或根据当地法律要求及时回复）。请提供足够的信息以核实您的身份，并明确说明您具体需要什么。</p>
			</div>

			<div class="bilingual-section">
				<p>To ensure the security of your personal information, when you make the above request to us, we may first verify your identity (such as adding verification, requiring you to provide a written request or other reasonable methods), and then process your request.</p>
				<p class="chinese">为保障您的账户及个人信息安全，当您提出上述请求时，我们可能会先对您的身份进行验证（例如增加验证、要求您提供书面请求或其他合理方式），然后处理您的请求。</p>
			</div>

			<div class="bilingual-section">
				<p>For your reasonable requests, we generally do not charge any fees. However, for repeated requests that exceed a reasonable limit, we may charge a certain fee at our discretion. We may refuse requests that are not directly related to your identity, are repeatedly applied for without reasonable grounds, or require excessive technical means (such as the need to develop new systems or fundamentally change current practices), pose risks to the legitimate rights and interests of others, or are impractical.</p>
				<p class="chinese">对于您提出的合理请求，我们通常不收取任何费用。但若重复请求超出合理范围，我们将酌情收取一定费用。对于与您的身份无关、无正当理由反复提出、需要过度技术手段（如需开发新系统或根本性改变现有做法）、可能损害他人合法权益或不切实际的请求，我们可能会予以拒绝。</p>
			</div>

			<!-- Section 5: Storage and Protection -->
			<h2>Storage and Protection of Information / 信息的储存与保存</h2>
			<div class="bilingual-section">
				<p>We keep your information only as long as necessary for our services in Dock2Gdansk platform and legal requirements. Information related to active inquiries is maintained for a reasonable period for service provision. Business requests and matching data are typically kept for 5 years to support ongoing business relationships and ensure legal compliance. Communication records are maintained for a period of 2 years for customer service purposes. Technical logs and analytics data are kept for 12 months for security and improvement purposes.</p>
				<p class="chinese">我们仅在Dock2Gdansk平台服务及法律要求所必需的期限内保存您的信息。账户有效期内将保留活跃账户信息，同时保留合理的服务提供时间。业务请求及匹配数据通常保存5年，以支持持续业务关系并确保法律合规。通信记录为客户服务目的保存2年。技术日志与分析数据为安全维护及优化目的保存12个月。</p>
			</div>

			<div class="bilingual-section">
				<p>You can request deletion of your information at any time, though some information may need to be retained for legal compliance or legitimate business purposes like contract fulfillment.</p>
				<p class="chinese">您可以随时要求删除您的信息，尽管某些信息可能需要保留以符合法律或合法的业务目的，如合同履行。</p>
			</div>

			<div class="bilingual-section">
				<p>The personal information we collect and generate during our operations within the territory of the People's Republic of China (Hong Kong Special Administrative Region) will be stored within China. If we need to provide your personal information to a third party outside China other than us, we will obtain your separate consent and fulfill the obligations stipulated by law, taking necessary measures to ensure that the activities of the overseas recipient in processing your personal information comply with the law.</p>
				<p class="chinese">我们在中华人民共和国境内开展业务期间收集和生成的个人信息将存储于中国境内（香港特别行政区）。如需向境外第三方提供您的个人信息，我们将另行征得您的同意，并履行法律规定的义务，采取必要措施确保境外接收方处理您个人信息的行为符合法律规定。</p>
			</div>

			<div class="bilingual-section">
				<p>We protect your information through the encryption of data both when it is stored and transmitted, regular security testing and vulnerability assessments, strict access controls that ensure only authorized personnel can access your data, employee training on data protection and security, and incident response plans to address any security issues promptly.</p>
				<p class="chinese">我们通过以下方式保护您的信息：对存储和传输的数据进行加密，定期安全测试和漏洞评估，严格的访问控制，只有授权人员才能访问您的数据，员工接受数据保护和安全培训，以及快速解决任何安全问题的突发事件响应计划。</p>
			</div>

			<div class="bilingual-section">
				<p>If we experience a data breach that could affect you, we'll notify you and relevant authorities as required by law, typically within 72 hours of discovery. We extensively use AWS infrastructure and are notified of any data breaches by email.</p>
				<p class="chinese">如果发生可能影响您的数据泄露事件，我们将根据法律规定在发现后的72小时内通知您和相关机构。我们广泛使用AWS基础设施，并通过电子邮件通知任何数据泄露事件。</p>
			</div>

			<!-- Section 6: Policy Updates -->
			<h2>Updates of This Policy / 政策更新</h2>
			<div class="bilingual-section">
				<p>To provide you with better product and service experience, we continually strive to enhance our products, services, and technologies. When new services or business process changes occur, we may update our privacy policy to inform you of the specific changes. However, without your explicit consent, we will not restrict the rights you enjoy under this policy.</p>
				<p class="chinese">为了给您提供更好的产品和服务体验，我们不断努力改进我们的产品、服务和技术。当有新的服务或业务流程变更时，我们可能会更新隐私政策，以告知您具体的变化。但是，如果没有您的明确同意，我们不会限制您在本政策下享有的权利。</p>
			</div>

			<div class="bilingual-section">
				<p>For major changes, we will also provide more prominent notifications (including through public announcements on the Dock2Gdansk platform or by offering you pop-up prompts).</p>
				<p class="chinese">对于重大变更，我们也将提供更突出的通知（包括通过Dock2Gdansk平台上的公共公告或向您提供弹出提示）。</p>
			</div>

			<div class="bilingual-section">
				<p>The major changes referred to in this policy include, but are not limited to:</p>
				<p class="chinese">本政策中提及的主要变更包括但不限于：</p>
				<ul>
					<li>The business model of the service has undergone significant changes. Such as the purpose of processing personal information, the types of personal information processed, and the way personal information is used;<br/>服务的商业模式发生了重大变化，例如处理个人信息的目的、处理个人信息的类型以及使用个人信息的方式；</li>
					<li>Changes in the privacy policy subject due to business adjustments, transactions or mergers and acquisitions, and the new subject recipient changes the original processing purpose and processing method;<br/>因业务调整、交易或并购等原因变更隐私政策主题，以及新的主题接收方改变原有处理目的和处理方式；</li>
					<li>The main objects of personal information sharing or public disclosure have changed;<br/>个人信息共享或公开的主要对象已经改变；</li>
					<li>There are significant changes in users' rights to personal information and the ways to exercise them;<br/>用户对个人信息的权利和行使权利的方式有重大变化；</li>
					<li>When the contact information of the person in charge of personal information protection and the complaint channels change;<br/>个人信息保护负责人信息及投诉渠道发生变更；</li>
					<li>When the personal information protection impact assessment report indicates that the product has a significant impact on an individual's rights and interests.<br/>当个人信息保护影响评估报告表明产品对个人权利、利益有重大影响时。</li>
				</ul>
			</div>

			<div class="bilingual-section">
				<p>We will also archive previous versions of this policy on a dedicated page on Dock2Gdansk platform for your reference.</p>
				<p class="chinese">我们还将本政策的先前版本存档在Dock2Gdansk平台的专用页面上，以供您参考。</p>
			</div>

			<!-- Section 7: Protection of Minors -->
			<h2>Protection of Minors / 未成年人保护</h2>
			<div class="bilingual-section">
				<p>Our platform is exclusively for business use and not intended for anyone under 18. We don't knowingly collect information from minors. If we discover we've collected such information, we'll delete it immediately. Meanwhile, if a minor provides us with personal information without the consent of his or her parents or guardians, the parents or guardians should contact <a href="mailto:info@dock2gdansk.com">info@dock2gdansk.com</a> to delete such personal information.</p>
				<p class="chinese">我们的平台专为商业用途设计，不向18岁以下的任何人开放。我们不会主动收集未成年人的信息。若发现已收集此类信息，我们将立即删除。同时，若未成年人未经其父母或监护人同意提供个人信息，父母或监护人应联系<a href="mailto:info@dock2gdansk.com">info@dock2gdansk.com</a>以删除此类个人信息。</p>
			</div>

			<!-- Section 8: Contact Us -->
			<h2>Contact Us / 联系我们</h2>
			<div class="bilingual-section contact-info">
				<p>For any privacy questions or to exercise your rights, contact <a href="mailto:info@dock2gdansk.com">info@dock2gdansk.com</a>. We're committed to addressing your concerns promptly and transparently.</p>
				<p class="chinese">如有任何隐私问题或需要行使您的权利，请联系<a href="mailto:info@dock2gdansk.com">info@dock2gdansk.com</a>。我们承诺及时、透明地解决您的问题。</p>
				<p>
					<strong>Data Protection Officer:</strong> <a href="mailto:iod@portgdansk.pl">iod@portgdansk.pl</a><br/>
					<strong>General Inquiries:</strong> <a href="mailto:info@dock2gdansk.com">info@dock2gdansk.com</a>
				</p>
				<p>If you're not satisfied with our response, you can contact your local data protection authority or privacy regulator.</p>
				<p class="chinese">如果您对我们的回复不满意，您可以联系当地的数据保护机构或隐私监管机构。</p>
			</div>

			<!-- Section 9: Supplementary Provisions -->
			<h2>Supplementary Provisions / 附则</h2>
			<div class="bilingual-section">
				<p>The interpretation of this policy and the resolution of disputes shall be governed by the laws of the People's Republic of China. Any disputes related to this policy (including your dissatisfaction with our response or your belief that our processing of your personal information has infringed upon your legitimate rights and interests) shall be resolved through friendly consultation between both parties. If the disputes cannot be resolved through negotiation, you may also seek a solution by filing a lawsuit with the competent court in the defendant's place of residence.</p>
				<p class="chinese">本政策的解释及争议解决均应适用中华人民共和国法律。与本政策相关的任何纠纷（包括您对我们的回复不满意，或您认为我们的个人信息处理行为损害了您的合法权益），双方应经友好协商解决；若不能协商解决，您还可以通过向被告住所地有管辖权的法院提起诉讼来寻求解决方案。</p>
			</div>

			<div class="bilingual-section">
				<p>If any court with jurisdiction determines or holds that any provision of this policy is invalid, such provision shall be removed from this policy, but the invalidity of such provision shall not affect the validity of the remaining provisions of this policy. The remaining provisions of this policy will continue to be implemented.</p>
				<p class="chinese">如果有管辖权的任何法院裁定或判决本政策的任何条款无效，则该条款将从本政策中移除，但该条款的无效不影响本政策其余条款的效力。本政策的其余条款将继续执行。</p>
			</div>

			<div class="bilingual-section">
				<p>The title of this policy is designed for ease of reading only and does not affect the meaning or interpretation of any provision of this policy.</p>
				<p class="chinese">本政策的标题仅为方便阅读而设计，不影响本政策任何条款的含义或解释。</p>
			</div>

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
		line-height: 1.8;
		color: #333;
		font-size: 16px;
	}

	h1 {
		font-size: 28px;
		margin-bottom: 8px;
		color: #000;
		font-weight: 600;
	}

	h1.chinese-title {
		font-size: 24px;
		margin-bottom: 24px;
		color: #333;
	}

	h2 {
		font-size: 22px;
		margin-top: 40px;
		margin-bottom: 20px;
		color: #000;
		border-bottom: 2px solid #0062ff;
		padding-bottom: 8px;
	}

	h3 {
		font-size: 18px;
		margin-top: 28px;
		margin-bottom: 16px;
		color: #000;
		font-weight: 600;
	}

	h4 {
		font-size: 16px;
		margin-top: 20px;
		margin-bottom: 12px;
		color: #333;
		font-weight: 600;
	}

	p {
		margin-bottom: 12px;
	}

	.date {
		font-style: italic;
		color: #666;
		margin-bottom: 32px;
		font-size: 14px;
	}

	.bilingual-section {
		margin-bottom: 24px;
		padding: 16px 0;
		border-bottom: 1px solid #e0e0e0;
	}

	.bilingual-section:last-child {
		border-bottom: none;
	}

	.bilingual-section p.chinese {
		color: #555;
		margin-top: 12px;
		padding-left: 16px;
		border-left: 3px solid #0062ff;
	}

	.attention-box {
		background: #fff8e1;
		padding: 20px;
		border-radius: 8px;
		border-left: 4px solid #ffc107;
	}

	.highlight-box {
		background: #e3f2fd;
		padding: 20px;
		border-radius: 8px;
		border-left: 4px solid #0062ff;
	}

	.toc-section {
		background: #f5f5f5;
		padding: 20px;
		border-radius: 8px;
	}

	.toc-list {
		list-style: none;
		padding: 0;
		margin: 16px 0 0 0;
	}

	.toc-list li {
		padding: 8px 0;
		border-bottom: 1px solid #e0e0e0;
	}

	.toc-list li:last-child {
		border-bottom: none;
	}

	ul {
		margin: 16px 0;
		padding-left: 24px;
	}

	ul li {
		margin-bottom: 12px;
		line-height: 1.6;
	}

	a {
		color: #0062ff;
		text-decoration: none;
	}

	a:hover {
		text-decoration: underline;
	}

	.contact-info p {
		margin-bottom: 16px;
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
			font-size: 24px;
		}

		h1.chinese-title {
			font-size: 20px;
		}

		h2 {
			font-size: 20px;
		}

		h3 {
			font-size: 16px;
		}

		.bilingual-section p.chinese {
			padding-left: 12px;
		}
	}

	/* Match main layout header styles */
	:global(.bx--header) {
		position: fixed !important;
		top: 0 !important;
		z-index: 1000 !important;
	}
</style>
