import { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.andrei.platformameteo',
  appName: 'Platforma Meteo',
  webDir: 'build',
  server: {
    androidScheme: 'http',
    cleartext: true
  }
};

export default config;