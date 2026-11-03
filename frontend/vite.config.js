import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        followRedirects: false,
      },
      '/uploads': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        followRedirects: false,
      },
      '/logos': {
        target: 'http://localhost:8000/uploads/logos',
        changeOrigin: true,
        followRedirects: false,
      },
      '/posters': {
        target: 'http://localhost:8000/uploads/posters',
        changeOrigin: true,
        followRedirects: false,
      },
      '/avatars': {
        target: 'http://localhost:8000/uploads/avatars',
        changeOrigin: true,
        followRedirects: false,
      },
    },
  },
})
