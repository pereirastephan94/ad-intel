import type { Metadata, Viewport } from 'next';
import './globals.css';
import Header from '@/components/site/Header';
import Footer from '@/components/site/Footer';
import { LeadProvider } from '@/components/ui/lead';
import StoryblokBridge from '@/components/site/StoryblokBridge';
import { getStory } from '@/lib/storyblok';

export const metadata: Metadata = {
  title: { default: 'UG Programme in Business, Entrepreneurship & AI | Scaler School of Business', template: '%s | SSB UG' },
  description:
    'A four-year UG programme in Business, Entrepreneurship & AI, on the Scaler campus in Bengaluru. Build real businesses, ship AI products and intern from Year 1.',
};

export const viewport: Viewport = { themeColor: '#068852' };

export default async function RootLayout({ children }: { children: React.ReactNode }) {
  const config = (await getStory('config'))?.content ?? ({} as any);
  return (
    <html lang="en">
      <body>
        <LeadProvider>
          <Header config={config} />
          <main>{children}</main>
          <Footer config={config} />
        </LeadProvider>
        <StoryblokBridge />
      </body>
    </html>
  );
}
