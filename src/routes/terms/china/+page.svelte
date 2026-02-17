<script>
	import { Button, Header, HeaderNav, HeaderNavItem } from 'carbon-components-svelte';
	import { t, currentLanguage, switchLanguage } from '$lib/stores/config.js';
	import { goto } from '$app/navigation';

	function handleLanguageSwitch(lang) {
		console.log('User manually switched to language:', lang);
		switchLanguage(lang);
		localStorage.setItem('language-override', 'true');
		localStorage.setItem('preferred-language', lang);
	}
</script>

<svelte:head>
	<title>Terms of Use for China - Dock2Gdansk | 中华人民共和国境内用户使用条款</title>
	<meta
		name="description"
		content="Dock2Gdansk Terms of Use for Users in the People's Republic of China - 中华人民共和国境内用户使用条款"
	/>
</svelte:head>

<Header company="Dock2Gdansk" platformName={t('site_tagline', 'Professional Cargo Transportation')}>
	<HeaderNav>
		<HeaderNavItem href="/" text={t('nav.home', 'Home')} />
		<HeaderNavItem onclick={() => handleLanguageSwitch('en')} text={t('EN', 'EN')} />
		<HeaderNavItem onclick={() => handleLanguageSwitch('zh')} text={t('中文', '中文')} />
	</HeaderNav>
</Header>

<section class="terms-content">
	<div class="content-wrapper">
		<div class="content-container">
			<h1>Terms of Use for Users in the People's Republic of China</h1>
			<h1 class="chinese-title">中华人民共和国境内用户使用条款</h1>

			<p class="date">Last Updated: January 2026 / 最后更新：2026年1月</p>

			<!-- Attention Notice -->
			<div class="bilingual-section attention-box">
				<p><strong>Attention:</strong> These Terms of Use govern the services provided by Zarząd Morskiego Portu Gdańsk SA through dock2gdansk.com ("Dock2Gdansk") to users located within the territory of the People's Republic of China. For Terms applicable to users outside the PRC, please refer to the <a href="/terms?region=global">general Terms of Use</a>.</p>
				<p class="chinese"><strong>请注意：</strong>本使用条款适用于Zarząd Morskiego Portu Gdańsk SA通过dock2gdansk.com（"Dock2Gdansk"）向中华人民共和国境内用户提供的服务。中华人民共和国境外用户的使用条款请参阅<a href="/terms?region=global">通用使用条款</a>。</p>
			</div>

			<!-- Quick Summary -->
			<div class="bilingual-section highlight-box">
				<h2>Quick Summary - What These Terms Mean</h2>
				<h2 class="chinese-heading">简要概述 - 本条款的含义</h2>
				<p>These terms govern your use of our B2B supplier matching platform (https://dock2gdansk.com). By using our service, you agree to provide accurate business information, use the platform for legitimate business purposes only, and respect other users' intellectual property. We facilitate connections between businesses but don't guarantee results or verify all information. You're responsible for your own business decisions and relationships. We may suspend access to the database for violations of these terms or involvement in fraudulent activity.</p>
				<p class="chinese">本条款规范您对我们B2B供应商匹配平台（https://dock2gdansk.com）的使用。使用我们的服务即表示您同意提供准确的商业信息，仅将平台用于合法商业目的，并尊重其他用户的知识产权。我们促进企业之间的联系，但不保证结果或验证所有信息。您需对自己的商业决策和关系负责。如违反本条款或涉及欺诈活动，我们可能会暂停您对数据库的访问权限。</p>
			</div>

			<!-- Key Points -->
			<div class="bilingual-section toc-section">
				<h3>Key Points / 要点：</h3>
				<ul class="toc-list">
					<li>Use our platform for legitimate B2B matching only / 仅将平台用于合法的B2B匹配</li>
					<li>Provide accurate information and keep it updated / 提供准确信息并保持更新</li>
					<li>Respect other users and don't spam or harass / 尊重其他用户，禁止发送垃圾信息或骚扰</li>
					<li>We facilitate connections but don't guarantee business outcomes / 我们促进联系但不保证商业成果</li>
					<li>You're responsible for your own business relationships and contracts / 您需对自己的商业关系和合同负责</li>
					<li>We can suspend access to shared information for violations of terms, with proper notice and appeal rights / 如违反条款，我们可暂停信息共享访问权限，并提供适当通知和申诉权利</li>
				</ul>
			</div>

			<!-- Section 1 -->
			<h2>1. Acceptance of Terms and Governing Law / 条款接受与适用法律</h2>
			<div class="bilingual-section">
				<p>1.1 By accessing or using Dock2Gdansk's B2B supplier matching platform (the "Platform"), you agree to be bound by these Terms of Use ("Terms"). These Terms form a legally binding agreement between you and Dock2Gdansk ("we," "us," or "our").</p>
				<p class="chinese">1.1 访问或使用Dock2Gdansk的B2B供应商匹配平台（"平台"）即表示您同意受本使用条款（"条款"）的约束。本条款构成您与Dock2Gdansk（"我们"）之间具有法律约束力的协议。</p>
			</div>

			<div class="bilingual-section">
				<p>1.2 If you're using the Platform on behalf of a business or organization, you represent that you have authority to bind that entity to these Terms. If you don't agree with any part of these Terms, you may not use our Platform.</p>
				<p class="chinese">1.2 如果您代表企业或组织使用本平台，即表示您有权使该实体受本条款约束。如果您不同意本条款的任何部分，则不得使用我们的平台。</p>
			</div>

			<div class="bilingual-section">
				<p>1.3 You may not access or use the services, the Platform, or accept the Terms if: (a) you have not reached the legal age required to enter into a binding contract with Dock2Gdansk's B2B; or (b) you are not permitted to accept any services under the laws of other countries (including the country where you reside or the country where you access and use the services and the Platform).</p>
				<p class="chinese">1.3 在下列情况下，您不得访问或使用服务、平台或接受本条款：(a) 您未达到与Dock2Gdansk B2B订立具有约束力合同所需的法定年龄；或 (b) 根据其他国家/地区的法律（包括您居住的国家/地区或您访问和使用服务及平台的国家/地区），您不被允许接受任何服务。</p>
			</div>

			<div class="bilingual-section legal-highlight">
				<p><strong>1.4</strong> These Terms are governed by Polish law for EU users and Chinese law for China users. For users in other jurisdictions, these Terms are governed by Polish law. However, mandatory consumer and business protection laws in your jurisdiction will override these Terms where applicable and cannot be waived.</p>
				<p class="chinese"><strong>1.4</strong> 本条款对欧盟用户适用波兰法律，对中国用户适用中国法律。对于其他司法管辖区的用户，本条款适用波兰法律。但您所在司法管辖区的强制性消费者和商业保护法律在适用情况下将优先于本条款，且不可放弃。</p>
			</div>

			<div class="bilingual-section">
				<p>1.5 We may update these Terms from time to time to reflect legal changes or service improvements. We'll provide at least 30 days' advance notice of material changes through email and prominent platform notifications. Your continued use after the notice period means you accept the updated Terms. If you do not accept the changes, you may terminate the sharing of your information before the changes take effect.</p>
				<p class="chinese">1.5 我们可能会不时更新本条款以反映法律变更或服务改进。我们将通过电子邮件和平台显著通知提前至少30天通知重大变更。通知期后继续使用即表示您接受更新后的条款。如果您不接受变更，可在变更生效前终止信息共享。</p>
			</div>

			<!-- Section 2 -->
			<h2>2. Description of Service and Service Level Commitments / 服务描述及服务水平承诺</h2>
			<div class="bilingual-section">
				<p>2.1 Our Platform connects businesses seeking suppliers with companies offering relevant products or services. We provide sophisticated matching algorithms, secure communication tools, and comprehensive market insights to facilitate successful B2B relationships. Our service includes maintaining detailed user profiles and business requirements, analyzing needs against our comprehensive supplier database, presenting relevant matches based on your specified criteria, facilitating secure initial communication between potential partners, and providing valuable market insights and industry trends.</p>
				<p class="chinese">2.1 我们的平台将寻找供应商的企业与提供相关产品或服务的公司连接起来。我们提供先进的匹配算法、安全的通信工具和全面的市场洞察，以促进成功的B2B关系。我们的服务包括维护详细的用户档案和业务需求、根据我们全面的供应商数据库分析需求、根据您指定的标准呈现相关匹配、促进潜在合作伙伴之间的安全初步沟通，以及提供有价值的市场洞察和行业趋势。</p>
			</div>

			<div class="bilingual-section">
				<p>2.2 We target 99.5% platform availability during business hours (9 AM to 6 PM local time) and 99% availability overall. Planned maintenance will be scheduled during off-peak hours with at least 48 hours' advance notice. We provide real-time service status updates.</p>
				<p class="chinese">2.2 我们的目标是在工作时间（当地时间上午9点至下午6点）实现99.5%的平台可用性，总体可用性达到99%。计划维护将安排在非高峰时段，并提前至少48小时通知。我们提供实时服务状态更新。</p>
			</div>

			<div class="bilingual-section">
				<p>2.3 We act strictly as a facilitator and technology provider. We don't manufacture products, provide services directly, participate in business transactions between users, guarantee the accuracy of user-provided information, or assume responsibility for business relationships formed through our Platform. All business relationships, contracts, and transactions are solely between the matched parties.</p>
				<p class="chinese">2.3 我们严格作为促进者和技术提供商。我们不制造产品、不直接提供服务、不参与用户之间的商业交易、不保证用户提供信息的准确性，也不对通过我们平台建立的商业关系承担责任。所有商业关系、合同和交易仅在匹配双方之间进行。</p>
			</div>

			<div class="bilingual-section">
				<p>2.4 We may initiate, change, upgrade, suspend or terminate any service (or any special feature of the service) or impose conditions on the service (or any special feature of the service) without prior notice.</p>
				<p class="chinese">2.4 我们可以在不事先通知的情况下启动、更改、升级、暂停或终止任何服务（或服务的任何特殊功能），或对服务（或服务的任何特殊功能）施加条件。</p>
			</div>

			<!-- Section 3 -->
			<h2>3. General rules for users / 用户一般规则</h2>
			<div class="bilingual-section">
				<p>3.1 As a condition of your access to and use of the Platform or services, you agree to comply with all applicable laws and regulations when accessing or using the website or services.</p>
				<p class="chinese">3.1 作为您访问和使用平台或服务的条件，您同意在访问或使用网站或服务时遵守所有适用的法律法规。</p>
			</div>

			<div class="bilingual-section">
				<p>3.2 You must be at least 18 years old and legally authorized to enter binding contracts in your jurisdiction. You must represent a legitimate, legally registered business entity or be genuinely seeking business services for commercial purposes. Personal use, non-commercial activities, or residential purchases are strictly prohibited.</p>
				<p class="chinese">3.2 您必须年满18周岁并在您所在司法管辖区具有签订具有约束力合同的法律授权。您必须代表合法注册的商业实体，或真正为商业目的寻求商业服务。严禁个人使用、非商业活动或住宅采购。</p>
			</div>

			<div class="bilingual-section">
				<p>3.3 You agree to prohibit the use of any content or material on the Platform for any purpose not expressly permitted in these Terms.</p>
				<p class="chinese">3.3 您同意禁止将平台上的任何内容或材料用于本条款未明确允许的任何目的。</p>
			</div>

			<div class="bilingual-section">
				<p>3.4 To learn how the Platform and its affiliates use and protect your personal information when you use the relevant websites, please visit the Dock2Gdansk platform <a href="/privacy/china">Privacy Policy</a>.</p>
				<p class="chinese">3.4 了解平台及其关联方在您使用相关网站时如何使用和保护您的个人信息，请访问Dock2Gdansk平台<a href="/privacy/china">隐私政策</a>。</p>
			</div>

			<div class="bilingual-section">
				<p>3.5 You agree that you will not take any action that would harm the integrity of the Platform and/or any other user's computer system or network, nor will you obtain unauthorized access to the Platform and/or any other user's computer system or network.</p>
				<p class="chinese">3.5 您同意不会采取任何损害平台和/或任何其他用户的计算机系统或网络完整性的行为，也不会未经授权访问平台和/或任何其他用户的计算机系统或网络。</p>
			</div>

			<div class="bilingual-section">
				<p>3.6 By posting or displaying any information, content or material on the Platform (any of such information, content or material, collectively referred to as "User Content") or providing any User Content to Dock2Gdansk and/or its affiliates and their respective representative(s), and to the extent permitted under applicable laws, you grant an irrevocable, perpetual, worldwide, royalty-free, and sub-licensable (through multiple tiers) license to Dock2Gdansk and/or its affiliates and their respective representative(s) to display, transmit, distribute, reproduce, publish, duplicate, adapt, modify, edit, translate, create derivative works using the User Content, remove any part of it (including, without limitation, the watermark or mark the User Content bears), and otherwise use any or all of the User Content in any form, media, or technology now known or not currently known in any manner, on the Platform, Dock2Gdansk and/or Third Party and for any purpose which may be beneficial, whether directly or indirectly, to Dock2Gdansk, the operation of the Platform, the provision of any services and promotion services and/or the business of the User. You confirm and warrant to Dock2Gdansk that you have all the rights, power and authority necessary to grant the above license and the User Content and use of such User Content (including derivative works) by Dock2Gdansk and/or its affiliates under such license is free from any infringement or violation of any Third Party Rights (as defined in clause 5.4 of the Terms). To the maximum extent permitted by law, you waive your right to enforce your Intellectual Property Rights in the User Content against Dock2Gdansk and/or its affiliates, assignees or sub-licensees in connection with use of such User Content in connection with the Services. Information that is protected under data protection laws will only be used and kept in compliance with those laws.</p>
				<p class="chinese">3.6 通过在平台上发布或展示任何信息、内容或材料（任何此类信息、内容或材料统称为"用户内容"）或向Dock2Gdansk和/或其关联方及其各自代表提供任何用户内容，在适用法律允许的范围内，您向Dock2Gdansk和/或其关联方及其各自代表授予不可撤销的、永久的、全球性的、免版税的、可分许可（通过多层）的许可，以在平台上以任何形式、媒体或技术展示、传输、分发、复制、出版、改编、修改、编辑、翻译、使用用户内容创建衍生作品、删除其任何部分（包括但不限于用户内容所附的水印或标记），以及以其他方式使用任何或全部用户内容。您向Dock2Gdansk确认并保证，您拥有授予上述许可所需的一切权利、权力和授权，且Dock2Gdansk和/或其关联方根据此许可使用用户内容（包括衍生作品）不侵犯或违反任何第三方权利（如本条款第5.4条所定义）。在法律允许的最大范围内，您放弃就与服务相关的用户内容使用向Dock2Gdansk和/或其关联方、受让人或分许可人主张知识产权的权利。受数据保护法保护的信息仅根据这些法律使用和保存。</p>
			</div>

			<!-- Section 4 -->
			<h2>4. Registration and Verification / 注册与验证</h2>
			<div class="bilingual-section">
				<p>4.1 When submitting an inquiry, you must provide accurate, complete, and current information including valid business contact information with verifiable email and phone numbers, accurate company details including registration numbers and industry classification, and legitimate business addresses and operational locations.</p>
				<p class="chinese">4.1 提交询盘时，您必须提供准确、完整和最新的信息，包括可验证的电子邮件和电话号码等有效的商业联系信息、包括注册号和行业分类在内的准确公司详情，以及合法的商业地址和运营地点。</p>
			</div>

			<div class="bilingual-section">
				<p>4.2 We implement multi-step verification procedures including validation against business registration databases, verification through third-party commercial data providers, direct contact verification with provided references, and review of submitted business documentation.</p>
				<p class="chinese">4.2 我们实施多步骤验证程序，包括与企业注册数据库的验证、通过第三方商业数据提供商的验证、与提供的推荐人的直接联系验证，以及对提交的商业文件的审核。</p>
			</div>

			<!-- Section 5 -->
			<h2>5. User's responsibility / 用户责任</h2>
			<div class="bilingual-section">
				<p>5.1 Each User represents, warrants and agrees that (a) you have full power and authority to accept the Terms, to grant the license and authorization and to perform the obligations hereunder; (b) your access and use the Platform and services will be for business purposes only; and (c) for users who are business entities, the address you provide when registering is the principal place of business of your business entity. For purposes of this provision, a branch or liaison office will not be considered a separate entity and your principal place of business will be deemed to be that of your head office.</p>
				<p class="chinese">5.1 每位用户声明、保证并同意：(a) 您拥有完全的权力和授权接受本条款、授予许可和授权并履行本条款规定的义务；(b) 您访问和使用平台及服务仅用于商业目的；(c) 对于作为商业实体的用户，您在注册时提供的地址是您商业实体的主要营业地点。就本条款而言，分支机构或联络处不视为独立实体，您的主要营业地点以总部所在地为准。</p>
			</div>

			<div class="bilingual-section">
				<p>5.2 User will be required to provide information or material about your entity, business or products/services as part of the registration process on the Platform for your access to and use of any service. Each user represents, warrants and agrees that (a) such information and material whether submitted during the inquiry process or thereafter throughout the continuation of the use of the Platform or service is true, accurate, current and complete, and (b) you will maintain and promptly amend all information and material to keep it true, accurate, current and complete.</p>
				<p class="chinese">5.2 作为平台注册流程的一部分，您需要提供关于您的实体、业务或产品/服务的信息或材料，以便您访问和使用任何服务。每位用户声明、保证并同意：(a) 无论是在询盘过程中提交的还是在使用平台或服务期间提交的此类信息和材料都是真实、准确、最新和完整的；(b) 您将维护并及时修改所有信息和材料以保持其真实、准确、最新和完整。</p>
			</div>

			<div class="bilingual-section">
				<p>5.3 Upon becoming an User, you consent to the inclusion of the contact information about you in our database and authorize Dock2Gdansk and our affiliates to share the contact information with other suppliers, customers or otherwise use your personal information in accordance with the <a href="/privacy/china">Privacy Policy</a>.</p>
				<p class="chinese">5.3 成为用户后，您同意将您的联系信息纳入我们的数据库，并授权Dock2Gdansk及其关联方与其他供应商、客户共享联系信息，或根据<a href="/privacy/china">隐私政策</a>以其他方式使用您的个人信息。</p>
			</div>

			<div class="bilingual-section">
				<p>5.4 Each User represents, warrants and agrees that (a) you shall be solely responsible for obtaining all necessary third party licenses and permissions regarding any User Content that you submit; (b) any User Content that you submit does not infringe or violate any of the intellectual property, trade secrets or any other personal or proprietary rights of any third party ("Third Party Rights"); and (c) you have the right and authority to sell, trade, distribute or export or offer to sell, trade, distribute or export the products or services described in the User Content and such sale, trade, distribution or export or offer does not violate any Third Party Right.</p>
				<p class="chinese">5.4 每位用户声明、保证并同意：(a) 您应独自负责获取与您提交的任何用户内容相关的所有必要的第三方许可和许可；(b) 您提交的任何用户内容不侵犯或违反任何第三方的知识产权、商业秘密或任何其他个人或专有权利（"第三方权利"）；(c) 您有权销售、交易、分销或出口或提议销售、交易、分销或出口用户内容中描述的产品或服务，且此类销售、交易、分销或出口或提议不违反任何第三方权利。</p>
			</div>

			<div class="bilingual-section">
				<p>5.5 Each User further represents, warrants and agrees that the User Content that you submit shall: a) be true, accurate, complete and lawful; b) not be false, misleading or deceptive; c) not contain information that is defamatory, libelous, threatening or harassing, obscene, objectionable, offensive, sexually explicit or harmful to minors; d) not contain information that is discriminatory or promotes discrimination based on race, sex, religion, nationality, disability, sexual orientation or age; e) not violate other Terms or any applicable additional agreements; f) not violate any applicable laws and regulations (including without limitation those governing export control, consumer protection, unfair competition, price gouging or false advertising, environmental protection or promote any activities which may violate any applicable laws and regulations; g) not contain any link directly or indirectly to any other web sites which includes any content that may violate the Terms.</p>
				<p class="chinese">5.5 每位用户进一步声明、保证并同意您提交的用户内容应：a) 真实、准确、完整和合法；b) 不得虚假、误导或欺骗；c) 不得包含诽谤、中伤、威胁或骚扰、淫秽、令人反感、冒犯性、色情或对未成年人有害的信息；d) 不得包含基于种族、性别、宗教、国籍、残疾、性取向或年龄的歧视性信息或宣传歧视；e) 不得违反其他条款或任何适用的附加协议；f) 不得违反任何适用的法律法规（包括但不限于出口管制、消费者保护、不正当竞争、价格欺诈或虚假广告、环境保护等法律法规）；g) 不得包含直接或间接链接到任何可能违反本条款内容的其他网站。</p>
			</div>

			<div class="bilingual-section">
				<p>5.6 Each User further represents, warrants and agrees that you may use our Platform exclusively to seek suppliers or customers for legitimate business purposes, share accurate and up-to-date information about your business needs or capabilities, communicate professionally and ethically with potential business partners, access market insights and data relevant to your industry and business operations, and utilize our matching algorithms to identify suitable business opportunities.</p>
			</div>

			<div class="bilingual-section">
				<p>5.7 Each User further represents, warrants and agrees that you may not post illegal, fraudulent, defamatory, or harmful content, infringe others' intellectual property rights or violate confidentiality obligations, attempt unauthorized access to our systems, interfere with Platform operations or disrupt other users' experience, use the Platform to directly compete with our services or develop competing platforms, engage in price manipulation, bid rigging, or other anti-competitive practices, or violate applicable trade sanctions, export controls, or anti-corruption laws.</p>
			</div>

			<div class="bilingual-section">
				<p>5.6 Each Member further represents, warrants and agrees that you shall/are a) not involve any scheme to undermine the integrity of the data, systems or networks used by Dock2Gdansk and/or any user of the Platform or gain unauthorized access to such data, systems or networks; b) not, and your director(s), officer(s), controlling party/ies, affiliates and legal jurisdiction in which any of the foregoing persons or entities is organized or has operations are not, persons or entities that are subject to any economic or fraud sanctions of any governmental, international or regulatory entities; and c) not engage in any activities that would otherwise create any liability for Dock2Gdansk or our affiliates.</p>
			</div>

			<div class="bilingual-section">
				<p>5.11 User acknowledges and agrees that the platform and services may only be used by businesses and their representatives for business use and not for individual consumers or for personal use.</p>
			</div>

			<div class="bilingual-section">
				<p>5.12 User acknowledges and agrees that each User is solely responsible for observing applicable laws and regulations in its respective jurisdictions to ensure that all access and use of the Platform and services are in compliance with the same.</p>
			</div>

			<!-- Prohibited Activities (5.13) -->
			<div class="bilingual-section highlight-box">
				<p><strong>5.13</strong> The following activities will result in immediate suspension or termination of information sharing through the platform. You may not:</p>
				<p class="chinese"><strong>5.13</strong> 以下活动将导致立即暂停或终止通过平台的信息共享。您不得：</p>
				<ul>
					<li>Provide false, misleading, outdated, or deliberately incomplete business information / 提供虚假、误导性、过时或故意不完整的商业信息</li>
					<li>Use the Platform for personal purchases, residential services, or non-commercial activities / 将平台用于个人购买、住宅服务或非商业活动</li>
					<li>Send spam, harassment, or unsolicited communications to other users / 向其他用户发送垃圾邮件、骚扰或未经请求的通信</li>
					<li>Attempt to bypass, manipulate, or reverse-engineer our matching algorithms / 试图绕过、操纵或逆向工程我们的匹配算法</li>
					<li>Collect, harvest, or scrape user information for purposes outside the Platform / 为平台外目的收集、获取或抓取用户信息</li>
					<li>Allow unauthorized third-party access, or deploy automated tools, bots, or scripts to access the Platform / 允许未经授权的第三方访问，或部署自动化工具、机器人或脚本访问平台</li>
				</ul>
			</div>

			<div class="bilingual-section">
				<p>5.14 All Platform interactions must maintain high professional standards. Users must honor good faith negotiations and preliminary agreements, provide honest assessments of business capabilities and requirements, respect confidential information shared during business discussions, promptly communicate material changes in business needs, capabilities, or circumstances, report suspected fraudulent activity or terms violations immediately, and comply with all applicable industry regulations and professional standards.</p>
			</div>

			<div class="bilingual-section">
				<p>5.15 If, at any time, you fail to meet any of the above requirements, you should stop using the services immediately. If Dock2Gdansk reasonably believes that any of your conduct violates or threatens to violate any applicable laws and regulations, Dock2Gdansk may, at its sole discretion, at any time take action as it may deem appropriate in light of the circumstances, including, but not limited to, terminating the provision of services to you, and suspending access to shared data, while reserving all rights it may have regarding any non-compliant actions or conduct of its members.</p>
			</div>

			<!-- Section 6 -->
			<h2>6. Breaches by Users / 用户违约</h2>
			<div class="bilingual-section">
				<p>6.1 Dock2Gdansk reserves the right in our sole discretion to remove, modify or reject any User content (in whole or in part) that you submit to the Platform which we reasonably believe (i) violates any applicable laws and regulations, (ii) violates the Terms hereunder, (iii) could subject Dock2Gdansk or our affiliates to liability, (iv) infringes any Third Party Rights, (v) could harm the interests of our users, third party or Dock2Gdansk or our affiliates, or (vi) is otherwise found inappropriate in Dock2Gdansk's sole discretion.</p>
				<p class="chinese">6.1 Dock2Gdansk保留自行决定删除、修改或拒绝您提交到平台的任何用户内容（全部或部分）的权利，如果我们合理认为该内容 (i) 违反任何适用的法律法规，(ii) 违反本条款，(iii) 可能使Dock2Gdansk或我们的关联方承担责任，(iv) 侵犯任何第三方权利，(v) 可能损害我们用户、第三方或Dock2Gdansk或我们关联方的利益，或 (vi) Dock2Gdansk自行认定为不当。</p>
			</div>

			<div class="bilingual-section">
				<p>6.2 If any User breaches any Terms, or if Dock2Gdansk has reasonable grounds to believe that a User is in breach of any Terms, Dock2Gdansk shall have the right to take such disciplinary actions as it deems appropriate, including without limitation: (i) suspending or terminating the sharing of information through the platform, at its sole discretion, without liability for any losses or damages arising out of or in connection with such suspension or termination.(ii) removing any product listings or other User content that the User has submitted; (iii) imposing other restrictions on the User's use of any features or functions of any Service as Dock2Gdansk may consider appropriate in its sole discretion; and (iv) any other corrective actions as Dock2Gdansk may deem necessary or appropriate in its sole discretion.</p>
				<p class="chinese">6.2 如果任何用户违反任何条款，或Dock2Gdansk有合理理由相信用户违反了任何条款，Dock2Gdansk有权采取其认为适当的纪律措施，包括但不限于：(i) 自行决定暂停或终止通过平台的信息共享，对由此产生的任何损失或损害不承担责任；(ii) 删除用户提交的任何产品列表或其他用户内容；(iii) 对用户使用任何服务的任何特性或功能施加Dock2Gdansk自行认为适当的其他限制；(iv) Dock2Gdansk自行认为必要或适当的任何其他纠正措施。</p>
			</div>

			<div class="bilingual-section">
				<p>6.3 Without limiting the generality of the provisions of the Terms, a User would be considered as being in breach of the Terms in any of the following circumstances: a) Dock2Gdansk has reasonable grounds to suspect that any information provided by the User is not current or complete or is untrue, inaccurate, or misleading, or b) Dock2Gdansk believes that the User's actions may cause financial loss or legal liability to Dock2Gdansk or our affiliates or any other Users.</p>
			</div>

			<div class="bilingual-section">
				<p>6.4 Dock2Gdansk reserves the right to cooperate fully with governmental or regulatory authorities, law enforcement bodies, private investigators and/or injured third parties in the investigation of any suspected criminal or civil wrongdoing. Further, to the extent permitted by applicable laws and policies, Dock2Gdansk may disclose the user's identity, contact information, and/or information shared through the platform or activities carried out on or via the Platform, if requested by a government, regulatory or law enforcement body or an injured third party, or as a result of a subpoena or other legal action. Dock2Gdansk shall not be liable for damages or results arising from such disclosure, and User agrees not to bring any action or claim against Dock2Gdansk for such disclosure.</p>
				<p class="chinese">6.4 Dock2Gdansk保留与政府或监管机构、执法机构、私人调查人员和/或受害第三方充分合作调查任何涉嫌刑事或民事不当行为的权利。此外，在适用法律和政策允许的范围内，如果政府、监管或执法机构或受害第三方请求，或因传票或其他法律行动，Dock2Gdansk可能会披露用户的身份、联系信息和/或通过平台共享的信息或在平台上进行的活动。Dock2Gdansk对因此类披露产生的损害或后果不承担责任，用户同意不因此类披露对Dock2Gdansk提起任何诉讼或索赔。</p>
			</div>

			<div class="bilingual-section">
				<p>6.6 Each Member agrees to indemnify Dock2Gdansk, our affiliates, directors, employees, agents and representatives and to hold them harmless, from any and all damages, losses, claims and liabilities (including legal costs on a full indemnity basis) which may arise from your submission, posting or display of any User content, from your access to or use of the Platform or services, or from your breach of the Terms or any Additional Agreements.</p>
			</div>

			<div class="bilingual-section">
				<p>6.7 Each User further agrees that Dock2Gdansk is not responsible, and shall have no liability to you or anyone else for any User content or other material transmitted through the Platform or services, including fraudulent, untrue, misleading, inaccurate, defamatory, offensive or illicit material and that the risk of damage from such User content or other material rests entirely with the User. Dock2Gdansk reserves the right to assume the exclusive defense and control of any matter otherwise subject to indemnification by the User, in which event the User shall cooperate with Dock2Gdansk in asserting any available defenses.</p>
			</div>

			<!-- Section 7 -->
			<h2>7. Potential Transactions / 潜在交易</h2>
			<div class="bilingual-section">
				<p>7.1 Through the Platform, Dock2Gdansk provides electronic web-based platforms for exchanging information between Users and potential counterparties of products and services. However, for any Services, Dock2Gdansk does not represent any counterparty in specific transactions. Dock2Gdansk does not control and is not liable or responsible for the quality, safety, lawfulness or availability of the transactions offered via the Platform, the ability of the counterparties to complete transactions.</p>
				<p class="chinese">7.1 通过平台，Dock2Gdansk提供基于网络的电子平台，用于用户与产品和服务的潜在交易对手之间交换信息。但是，对于任何服务，Dock2Gdansk不代表特定交易中的任何交易对手。Dock2Gdansk不控制也不对通过平台提供的交易的质量、安全性、合法性或可用性，以及交易对手完成交易的能力负责。</p>
			</div>

			<div class="bilingual-section attention-box">
				<p>7.2 Users are hereby made aware that there may be risks of dealing with people acting under false pretenses. We encourage you to use various means, as well as common sense, to evaluate with whom you are dealing.</p>
				<p class="chinese">7.2 特此提醒用户，与假冒身份的人交易可能存在风险。我们鼓励您使用各种方法以及常识来评估您的交易对象。</p>
			</div>

			<div class="bilingual-section">
				<p>7.3 Users accessing or using the Platform or services shall assume the risks of conducting any transactions in connection with or through the Platform or services. Users accessing or using the Platform or services shall also fully assume all risks of liability or harm of any kind arising out of or in connection with any subsequent activity relating to the transactions. Examples of such risks shall include, but are not limited to, mis-representation of products and services, fraudulent schemes, unsatisfactory product quality, failure to meet specifications, defective or dangerous products, unlawful products, delay or default in delivery or payment, cost mis-calculations, breach of warranty, breach of contract, transportation accidents, the risk that the manufacture, importation, export, distribution, offer, display, purchase, sale and/or use of products or services may violate or may be asserted to violate Third Party Rights, and the risk that Users may incur costs of defense or other costs in connection with third parties' assertion of Third Party Rights, or in connection with any claims by any party that they are entitled to defense or indemnification in relation to the assertion of rights, demands or claims by claimants of Third Party Rights. All of the foregoing risks are referred to as "Transaction Risks". Dock2Gdansk is not liable or responsible for any damages, claims, liabilities, costs, harm, inconveniences, business disruptions or expenditures of any kind that may arise a result of or in connection with any Transaction Risks.</p>
				<p class="chinese">7.3 访问或使用平台或服务的用户应承担与平台或服务相关或通过平台或服务进行任何交易的风险。访问或使用平台或服务的用户还应完全承担与交易相关的任何后续活动产生的或与之相关的任何责任或损害风险。Dock2Gdansk对因任何交易风险产生的或与之相关的任何损害、索赔、责任、成本、伤害、不便、业务中断或支出不承担责任。</p>
			</div>

			<div class="bilingual-section">
				<p>7.6 In the event that any User has a dispute with any party to a transaction, such User agrees to release and indemnify Dock2Gdansk (and our agents, affiliates, directors, officers and employees) from all claims, demands, actions, proceedings, costs, expenses and damages (including without limitation any actual, special, incidental or consequential damages) arising out of or in connection with such dispute or the transaction.</p>
			</div>

			<!-- Section 8 -->
			<h2>8. Content Rights and Intellectual Property Protection / 内容权利与知识产权保护</h2>
			<div class="bilingual-section">
				<p>8.1 You retain full ownership of all content you submit to the Platform including business descriptions, service requirements, and communications. By posting content, you grant us a limited, worldwide, royalty-free license to use, display, reproduce, and distribute your content solely for the purpose of providing and improving Platform services.</p>
				<p class="chinese">8.1 您保留对提交到平台的所有内容的完全所有权，包括业务描述、服务需求和通信。通过发布内容，您授予我们有限的、全球性的、免版税的许可，仅为提供和改进平台服务而使用、展示、复制和分发您的内容。</p>
			</div>

			<div class="bilingual-section">
				<p>8.2 This license includes the right to process your content through our matching algorithms, display relevant portions to potential business partners, store content in our systems and backups, and analyze content patterns to improve service quality. The license terminates when you delete the content, though we may retain copies as required by law or legitimate business needs.</p>
				<p class="chinese">8.2 此许可包括通过我们的匹配算法处理您的内容、向潜在商业伙伴展示相关部分、在我们的系统和备份中存储内容以及分析内容模式以提高服务质量的权利。当您删除内容时许可终止，但我们可能会根据法律或合法商业需要保留副本。</p>
			</div>

			<div class="bilingual-section">
				<p>8.3 You're solely responsible for ensuring you have proper rights to share all information you provide. You must not post content that violates applicable laws or regulations, infringes intellectual property rights of third parties, contains confidential information you're not authorized to disclose, includes malicious code, viruses, or harmful links, or violates professional obligations or industry standards.</p>
			</div>

			<div class="bilingual-section">
				<p>8.4 The Platform, including its design, matching algorithms, software architecture, user interface, branding, and proprietary methodologies, constitutes our intellectual property or is licensed to us under appropriate agreements. Our matching algorithms, market analysis tools, and business methodologies are proprietary trade secrets protected by applicable intellectual property laws.</p>
				<p class="chinese">8.4 平台，包括其设计、匹配算法、软件架构、用户界面、品牌和专有方法，构成我们的知识产权或根据适当的协议许可给我们。我们的匹配算法、市场分析工具和业务方法是受适用知识产权法保护的专有商业秘密。</p>
			</div>

			<div class="bilingual-section">
				<p>8.5 You may not copy, modify, distribute, reverse engineer, or create derivative works from our Platform or proprietary systems. You may not use our trademarks, logos, or branding without explicit written permission. Violation of our intellectual property rights may result in legal action.</p>
				<p class="chinese">8.5 您不得复制、修改、分发、逆向工程或从我们的平台或专有系统创建衍生作品。未经明确书面许可，您不得使用我们的商标、标志或品牌。侵犯我们的知识产权可能导致法律诉讼。</p>
			</div>

			<div class="bilingual-section">
				<p>8.6 To the largest extent permissible under applicable law, all rights, title and interest to all derivative work created by Dock2Gdansk and/or its affiliates using User content pursuant to the Terms shall belong to Dock2Gdansk, which may be freely assignable, licensable or grantable by Dock2Gdansk to any third party or its affiliates.</p>
			</div>

			<!-- Section 9: Limitation of Liability -->
			<h2>9. Limitation of Liability / 责任限制</h2>
			<div class="bilingual-section">
				<p>9.1 We facilitate business connections but make no guarantees about match quality, business outcomes, partner reliability, or transaction success. We implement reasonable verification measures but don't independently verify all user information, business claims, or financial capabilities of Platform users.</p>
				<p class="chinese">9.1 我们促进商业联系，但不保证匹配质量、商业成果、合作伙伴可靠性或交易成功。我们实施合理的验证措施，但不独立验证所有用户信息、商业声明或平台用户的财务能力。</p>
			</div>

			<div class="bilingual-section">
				<p>9.2 To the maximum extent permitted by law, Dock2Gdansk makes no representations or warranties about the validity, accuracy, correctness, reliability, quality, stability, completeness, or currentness of any information provided on or through the Platform, and Dock2Gdansk makes no representations or warranties of any kind concerning any service offered on the Platform. Users acknowledge that business relationships inherently carry commercial risks that are outside our control. Users are solely responsible for conducting appropriate due diligence on potential partners, verifying credentials, capabilities, and business legitimacy, negotiating suitable contract terms and protection mechanisms, ensuring compliance with applicable industry regulations, and managing ongoing business relationships and dispute resolution.</p>
				<p class="chinese">9.2 在法律允许的最大范围内，Dock2Gdansk不对平台上或通过平台提供的任何信息的有效性、准确性、正确性、可靠性、质量、稳定性、完整性或时效性作出任何陈述或保证，也不对平台上提供的任何服务作出任何类型的陈述或保证。用户确认商业关系本身固有的商业风险超出我们的控制范围。用户独自负责对潜在合作伙伴进行适当的尽职调查、验证资质、能力和商业合法性、协商适当的合同条款和保护机制、确保遵守适用的行业法规，以及管理持续的商业关系和争议解决。</p>
			</div>

			<div class="bilingual-section">
				<p>9.3 Any material and information obtained through the Platform or services is done at each User's sole discretion and risk and each User is solely responsible for any damage to its own.</p>
			</div>

			<div class="bilingual-section">
				<p>9.4 No advice or information, whether oral or written, obtained by any User from Dock2Gdansk or through or from the Platform shall create any warranty not expressly stated herein.</p>
			</div>

			<div class="bilingual-section">
				<p>9.5 Each User hereby agrees to indemnify and hold Dock2Gdansk, our affiliates, directors, officers and employees harmless, from any and all losses, claims, liabilities (including legal costs on a full indemnity basis) which may arise from such User's access to or use of the Platform or services or from your breach of any of the representations, warranties hereunder and the terms and conditions of the Terms. Each User hereby further agrees to indemnify and hold Dock2Gdansk, our affiliates, directors, officers and employees harmless, from any and all losses, damages, claims, liabilities (including legal costs on a full indemnity basis) which may arise from User's breach of any representations and warranties made by User to Dock2Gdansk, including but not limited to those set forth in clause 5 hereunder.</p>
			</div>

			<div class="bilingual-section">
				<p>9.5 Each User hereby further agrees to indemnify and save Dock2Gdansk, our affiliates, directors, officers and employees harmless, from any and all losses, damages, claims, liabilities (including legal costs on a full indemnity basis) which may arise, directly or indirectly, as a result of any claims asserted by Third Party Rights claimants or other third parties relating to the User content, information and/or products offered. Each User hereby further agrees that Dock2Gdansk is not responsible and shall have no liability to you, for any material posted by others, including defamatory, offensive or illicit material and that the risk of damages from such material rests entirely with each User. Dock2Gdansk reserves the right, to assume the exclusive defense and control of any matter otherwise subject to indemnification by you, in which event you shall cooperate with Dock2Gdansk in asserting any available defenses.</p>
			</div>

			<div class="bilingual-section">
				<p>8.7 Dock2Gdansk shall not be liable for any special, direct, indirect, punitive, incidental or consequential damages or any damages whatsoever (including but not limited to damages for loss of profits or savings, business interruption, loss of information), whether in contract, negligence, tort, equity or otherwise or any other damages resulting from any of the following: a) the use or the inability to use the Platform or services; b) violation of Third Party Rights or claims or demands that User's manufacture, importation, exportation, distribution, offer, display, purchase, sale and/or use of products or services offered on the Platform or through the services may violate or may be asserted to violate Third Party Rights; or claims by any party that they are entitled to defense or indemnification in relation to assertions of rights, demands or claims by Third Party Rights claimants; c) unauthorized access by third parties to data or private information of any User; d) statements or conduct of any User of the Platform or services; or; f) any matters relating to the Platform or services, however arising, including negligence.</p>
				<p class="chinese">8.7 Dock2Gdansk对任何特殊的、直接的、间接的、惩罚性的、附带的或后果性的损害或任何损害（包括但不限于利润或储蓄损失、业务中断、信息丢失的损害）不承担责任，无论是在合同、过失、侵权、衡平法或其他方面，或因以下原因造成的任何其他损害：a) 使用或无法使用平台或服务；b) 侵犯第三方权利；c) 第三方未经授权访问任何用户的数据或私人信息；d) 平台或服务的任何用户的声明或行为；f) 与平台或服务相关的任何事项，无论如何产生，包括过失。</p>
			</div>

			<div class="bilingual-section">
				<p>8.8 The limitations and exclusions of liability to you under the Terms shall apply to the maximum extent permitted by law and shall apply whether or not Dock2Gdansk has been advised of or should have been aware of the possibility of any such losses arising.</p>
			</div>

			<!-- Section 9: Platform Availability -->
			<h2>9. Platform Availability, Service Modifications and Force Majeure / 平台可用性、服务修改和不可抗力</h2>
			<div class="bilingual-section">
				<p>9.1 Dock2Gdansk strives to maintain high Platform availability and target 99.5% uptime during standard business hours and 99% overall availability. We may experience occasional downtime for essential maintenance, security updates, or technical improvements. Planned maintenance will be scheduled during off-peak hours with at least 48 hours' advance notice through email and platform notifications.</p>
				<p class="chinese">9.1 Dock2Gdansk努力保持高平台可用性，目标是在标准工作时间内达到99.5%的正常运行时间和99%的总体可用性。我们可能会因必要的维护、安全更新或技术改进而偶尔停机。计划维护将安排在非高峰时段，并通过电子邮件和平台通知提前至少48小时告知。</p>
			</div>

			<div class="bilingual-section">
				<p>9.2 In cases of emergency maintenance, security incidents, or technical failures, Dock2Gdansk will work to restore service as quickly as possible and provide regular status updates. Dock2Gdansk maintain comprehensive backup systems and disaster recovery procedures to minimize service disruptions.</p>
			</div>

			<div class="bilingual-section">
				<p>9.3 Dock2Gdansk continuously improve our Platform and may modify, update, add, or discontinue features at any time to enhance user experience, comply with legal requirements, or address security concerns. Dock2Gdansk will provide reasonable advance notice for significant changes that materially affect service functionality, typically 30 days for major feature removals or substantial workflow changes.</p>
			</div>

			<div class="bilingual-section">
				<p>9.4 Dock2Gdansk shall not be liable for or required to pay compensation of any nature whatsoever for any loss arising from the unavailability, inconvenience or failures of the services or systems due to the following reasons: (i) system shut-down for maintenance; (ii) inability to transmit data due to failures in communications terminals or telecommunications equipment; (iii) systems failure and inability to perform its functions due to force majeure events including but not limited to typhoons, earthquakes, tsunamis, floods, power failure, fires, storms, war, political unrest, labour strikes, shortage of labor or materials, riots, insurrections, civil disturbances, terrorist attack, explosions, acts of God, governmental actions, orders of domestic or foreign courts or tribunals, non-performance of third parties; or (iv) suspension or delay of services or systems failure due to reasons beyond the reasonable control of Dock2Gdansk such as hacker or cyber attacks, technical adjustments or failure of the telecommunications department, website upgrades, third party problems or any suspension or disruption of transportation or business operation (including but not limited to delays or disruption of the resumption of work or operation ordered by any government agency) in the event of a national or regional spread of epidemic or pandemic.</p>
				<p class="chinese">9.4 Dock2Gdansk对因以下原因导致的服务或系统不可用、不便或故障造成的任何损失不承担责任或不需支付任何性质的赔偿：(i) 系统维护关闭；(ii) 因通信终端或电信设备故障无法传输数据；(iii) 因不可抗力事件导致的系统故障和无法执行其功能，包括但不限于台风、地震、海啸、洪水、停电、火灾、风暴、战争、政治动乱、劳资纠纷、劳动力或材料短缺、暴乱、起义、内乱、恐怖袭击、爆炸、天灾、政府行为、国内外法院或法庭命令、第三方不履行；或 (iv) 因超出Dock2Gdansk合理控制的原因导致的服务暂停或延迟或系统故障，如黑客或网络攻击、电信部门的技术调整或故障、网站升级、第三方问题或在全国或地区性流行病或大流行病蔓延时交通或业务运营的任何暂停或中断（包括但不限于任何政府机构命令的恢复工作或运营的延迟或中断）。</p>
			</div>

			<!-- Section 10 -->
			<h2>10. Comprehensive Compliance and Regulatory Framework / 全面合规与监管框架</h2>
			<div class="bilingual-section">
				<p>10.1 All Platform users must comply with applicable anti-corruption laws including the US Foreign Corrupt Practices Act (FCPA), UK Bribery Act, Anti-Money Laundering Law of the People's Republic of China, and equivalent laws in other jurisdictions. Users must not offer, pay, or accept bribes or improper payments, engage in facilitation payments or kickbacks, or violate local anti-corruption regulations.</p>
				<p class="chinese">10.1 所有平台用户必须遵守适用的反腐败法律，包括美国《反海外腐败法》（FCPA）、英国《贿赂法》、《中华人民共和国反洗钱法》以及其他司法管辖区的同等法律。用户不得提供、支付或接受贿赂或不当付款，不得从事便利费或回扣，或违反当地反腐败法规。</p>
			</div>

			<div class="bilingual-section">
				<p>10.2 We screen users against applicable sanctions lists including OFAC, EU sanctions lists, and Chinese regulatory lists. Users must comply with all applicable export control laws and trade sanctions. We may immediately halt data sharing with organizations that are listed on sanctions lists or involved in prohibited activities.</p>
				<p class="chinese">10.2 我们根据适用的制裁名单筛查用户，包括OFAC、欧盟制裁名单和中国监管名单。用户必须遵守所有适用的出口管制法律和贸易制裁。我们可能会立即停止与被列入制裁名单或参与禁止活动的组织的数据共享。</p>
			</div>

			<!-- Section 11 -->
			<h2>11. Dispute Resolution and Legal Framework / 争议解决与法律框架</h2>
			<div class="bilingual-section">
				<p>11.1 Before initiating formal legal proceedings, parties must attempt good faith resolution through our internal dispute mechanism. Submit disputes to <a href="mailto:info@dock2gdansk.com">info@dock2gdansk.com</a> with detailed descriptions of the issue, relevant supporting documentation, and proposed resolution. We'll facilitate resolution discussions and provide written responses within 30 days.</p>
				<p class="chinese">11.1 在启动正式法律程序之前，双方必须通过我们的内部争议机制尝试善意解决。请向<a href="mailto:info@dock2gdansk.com">info@dock2gdansk.com</a>提交争议，并附上问题的详细描述、相关支持文件和拟议解决方案。我们将促进解决讨论并在30天内提供书面回复。</p>
			</div>

			<div class="bilingual-section">
				<p>11.2 For EU Users: Disputes will be resolved through the courts of Poland or through EU-approved alternative dispute resolution mechanisms. EU users retain access to the European Commission's Online Dispute Resolution platform for cross-border disputes.</p>
			</div>

			<div class="bilingual-section legal-highlight">
				<p><strong>11.3 For China Users:</strong> Disputes will be resolved through Chinese courts with competent jurisdiction or through China International Economic and Trade Arbitration Commission (CIETAC) arbitration if both parties agree.</p>
				<p class="chinese"><strong>11.3 中国用户：</strong>争议将通过有管辖权的中国法院解决，或在双方同意的情况下通过中国国际经济贸易仲裁委员会（CIETAC）仲裁解决。</p>
			</div>

			<!-- Section 12 -->
			<h2>12. Contact Information and Support / 联系信息与支持</h2>
			<div class="bilingual-section">
				<p>12.1 All legal notices or demands to or upon a User shall be effective if either delivered personally, sent by email to the last-known email address provided by the User to Dock2Gdansk, or by posting such notice or demand on an area of the Platform that is publicly accessible without a charge. Notice to a User shall be deemed to be received by such User if and when: a) Dock2Gdansk is able to demonstrate that communication in electronic form, has been sent to such User, or b) immediately upon Dock2Gdansk posting such notice on an area of the Platform that is publicly accessible without charge.</p>
				<p class="chinese">12.1 如果通过亲自递送、发送电子邮件至用户向Dock2Gdansk提供的最后已知电子邮件地址，或在平台可免费公开访问的区域发布此类通知或要求，则向用户发出的所有法律通知或要求均为有效。在以下情况下，通知视为已被用户收到：a) Dock2Gdansk能够证明电子形式的通信已发送至该用户，或 b) Dock2Gdansk在平台可免费公开访问的区域发布此类通知后立即生效。</p>
			</div>

			<div class="bilingual-section">
				<p>12.2 You agree that all agreements, notices, requests, disclosures, and other communications sent to you by Dock2Gdansk in electronic form satisfy any legal requirement that such communications be in writing.</p>
			</div>

			<div class="bilingual-section contact-info">
				<h3>12.3 Contact Information / 联系方式</h3>
				<ul>
					<li><strong>General Terms Questions / 一般条款问题：</strong> <a href="mailto:info@dock2gdansk.com">info@dock2gdansk.com</a></li>
					<li><strong>Service Support / 服务支持：</strong> <a href="mailto:info@dock2gdansk.com">info@dock2gdansk.com</a></li>
					<li><strong>Privacy and Data Protection / 隐私和数据保护：</strong> <a href="mailto:iod@portgdansk.pl">iod@portgdansk.pl</a></li>
					<li><strong>Intellectual Property Issues / 知识产权问题：</strong> <a href="mailto:info@dock2gdansk.com">info@dock2gdansk.com</a></li>
					<li><strong>Compliance and Regulatory / 合规与监管：</strong> <a href="mailto:info@dock2gdansk.com">info@dock2gdansk.com</a></li>
				</ul>
			</div>

			<div class="bilingual-section">
				<h3>12.4 Regional Contacts / 区域联系方式</h3>
				<p><strong>Business Address / 商业地址：</strong> Gdansk, Poland / 波兰格但斯克</p>
				<p>For urgent issues affecting Platform security or user safety, contact <a href="mailto:info@dock2gdansk.com">info@dock2gdansk.com</a> for immediate assistance.</p>
				<p class="chinese">如有影响平台安全或用户安全的紧急问题，请联系<a href="mailto:info@dock2gdansk.com">info@dock2gdansk.com</a>获得即时帮助。</p>
			</div>

			<!-- Back to Home -->
			<div class="back-button">
				<Button kind="primary" on:click={() => goto('/')}>← Back to Homepage / 返回首页</Button>
			</div>
		</div>
	</div>
</section>

<style>
	.terms-content {
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

	h2.chinese-heading {
		font-size: 18px;
		margin-top: 8px;
		margin-bottom: 16px;
		color: #555;
		border-bottom: none;
		padding-bottom: 0;
	}

	h3 {
		font-size: 18px;
		margin-top: 28px;
		margin-bottom: 16px;
		color: #000;
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

	.legal-highlight {
		background: #fff3e0;
		padding: 20px;
		border-radius: 8px;
		border-left: 4px solid #ff9800;
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

	.contact-info {
		background: #f8f9fa;
		padding: 20px;
		border-radius: 8px;
		margin: 16px 0;
	}

	.contact-info h3 {
		margin-top: 0;
		margin-bottom: 16px;
	}

	.contact-info ul {
		margin: 0 0 16px 0;
		padding-left: 0;
		list-style: none;
	}

	.contact-info li {
		margin-bottom: 8px;
	}

	.back-button {
		text-align: center;
		margin-top: 48px;
		padding-top: 32px;
		border-top: 1px solid #e0e0e0;
	}

	/* Mobile responsive adjustments */
	@media (max-width: 768px) {
		.terms-content {
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
