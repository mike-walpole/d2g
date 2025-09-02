# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Dock2Gdansk (d2g) is a multilingual cargo transportation web application built with SvelteKit 2 (Svelte 5), deployed on Vercel with AWS backend infrastructure. The project supports English and Chinese localization through Paraglide.js and uses IBM Carbon Design System components.

## Common Development Commands

```bash
# Development
npm run dev                 # Start development server
npm run dev -- --open     # Start dev server and open browser

# Build and Preview
npm run build              # Build for production
npm run preview           # Preview production build

# Code Quality
npm run lint              # Run ESLint and Prettier checks
npm run format           # Format code with Prettier

# Setup
npm install              # Install dependencies
npm run prepare         # Sync SvelteKit (runs automatically)
```

## Architecture Overview

### Frontend Stack
- **SvelteKit 2** with **Svelte 5** (using new runes syntax)
- **Tailwind CSS v4** with Carbon Design System components
- **Paraglide.js** for internationalization (i18n)
- **Vercel adapter** for deployment

### Backend Infrastructure (AWS)
Located in `/infra/` directory:
- **API Gateway** + **Lambda functions** for backend API
- **DynamoDB** for data storage (form submissions, schemas)
- **Cognito** for authentication
- **SES** for email notifications
- Deployed in Hong Kong region (`ap-east-1`)

### Key Directories
```
src/
├── lib/
│   ├── assets/           # Static assets (favicon, etc.)
│   ├── paraglide/        # Generated i18n files (auto-generated)
│   └── stores/
│       └── config.js     # Global config, translations, API client
├── routes/
│   ├── +layout.svelte    # Main layout with Carbon header/footer
│   ├── +page.svelte      # Homepage
│   ├── kapitanat/        # Admin dashboard routes
│   ├── privacy/          # Privacy policy page
│   └── terms/            # Terms of service page
└── hooks.server.js       # Paraglide middleware setup

infra/                    # AWS CDK infrastructure
├── d2g_stack.py         # Main CDK stack definition
├── lambda/              # Lambda function code
└── schemas/             # DynamoDB schema definitions
```

## Key Implementation Details

### Internationalization
- Uses Paraglide.js for compile-time i18n
- Configuration in `project.inlang/` directory
- Generated files in `src/lib/paraglide/` (do not edit manually)
- Translation helper function `t()` in `src/lib/stores/config.js`
- Language switching via header navigation

### State Management
- Svelte 5 runes for component state
- Global stores in `src/lib/stores/config.js`:
  - `currentLanguage`: Current UI language
  - `configData`: API configuration data
  - `translations`: Derived translation data
  - `apiBaseUrl`: AWS API Gateway endpoint

### API Integration
- Backend API hosted on AWS API Gateway
- Base URL configured in `config.js` store
- Supports dynamic configuration loading via `/config` endpoint
- Error handling for API failures with fallbacks

### Carbon Design System
- Uses `carbon-components-svelte` for UI components
- Custom styling in `+layout.svelte` for header positioning
- Global CSS overrides for Carbon component customization

### Routing
- File-based routing via SvelteKit conventions
- Protected admin routes under `/kapitanat/`
- Static pages for legal content (`/privacy`, `/terms`)

## Development Guidelines

### Component Development
- Use Svelte 5 syntax with runes (`$state`, `$derived`, `$props`)
- Follow Carbon Design System patterns
- Include proper i18n support using `t()` helper
- Maintain responsive design principles

### Code Style
- ESLint + Prettier configuration included
- Tailwind CSS for custom styling
- Use Carbon components where possible
- Follow existing naming conventions

### Backend Development
When working with AWS infrastructure:
- CDK stack defined in `infra/d2g_stack.py`
- Lambda functions in `infra/lambda/`
- Deploy using `./deploy.sh` script
- Test endpoints locally before deployment

### Deployment
- Frontend: Vercel (configured with `@sveltejs/adapter-vercel`)
- Backend: AWS (CDK deployment)
- Environment-specific configurations handled via API

## API Endpoints

The AWS backend provides:
- `GET /config?type=all&lang={language}` - Get translations and configuration
- Form submission endpoints (see infra README for details)
- Admin dashboard endpoints (protected by Cognito)

## Troubleshooting

### Common Issues
1. **i18n not updating**: Check if Paraglide files need regeneration
2. **Carbon components not styling**: Verify CSS imports in `+layout.svelte`
3. **API connection issues**: Check `apiBaseUrl` in config store
4. **Build failures**: Run `npm run prepare` to sync SvelteKit

### Development Server
- Hot module replacement enabled
- API proxy may be needed for local backend testing
- Check browser console for i18n loading errors