import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  
  // Development server configuration
  server: {
    host: '0.0.0.0',
    port: 5173,
    watch: {
      usePolling: true,
    },
  },
  
  // Build optimization
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: false,
    minify: 'esbuild', // Changed from 'terser' to 'esbuild'
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          router: ['react-router-dom'],
          utils: ['axios']
        }
      }
    },
    // Optimize chunk size
    chunkSizeWarningLimit: 1000,
  },
  
  // Preview server (for testing production build)
  preview: {
    host: '0.0.0.0',
    port: 4173,
  },
  
  // Environment variables
  define: {
    // These will be replaced at build time
    __APP_VERSION__: JSON.stringify(process.env.npm_package_version),
  },
})
