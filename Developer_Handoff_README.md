Talent Strategy Dashboard - 2025 Review

This is a React-based dashboard for the People Strategy team. It visualizes workforce velocity, retention risk, and strategic recommendations based on 2025 metrics.

Tech Stack

Framework: React (Vite recommended)

Styling: Tailwind CSS

Charts: Recharts

Icons: Lucide React

Quick Start (For Developers)

Initialize Project

npm create vite@latest talent-dashboard -- --template react
cd talent-dashboard


Install Dependencies
Copy the package.json below or run:

npm install recharts lucide-react prop-types
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p


Configure Tailwind
Update tailwind.config.js:

export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}


Add the Dashboard

Replace the contents of src/App.jsx with the dashboard code provided.

Ensure Tailwind directives are in src/index.css:

@tailwind base;
@tailwind components;
@tailwind utilities;


Run Locally

npm run dev


Deployment

This app is a static single-page application (SPA). It can be easily deployed to:

Vercel / Netlify

AWS S3 + CloudFront

Internal Nginx servers