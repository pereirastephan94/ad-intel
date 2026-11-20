import StoryPage, { storyMetadata } from '@/components/site/StoryPage';

export const revalidate = 60;
export const generateMetadata = () => storyMetadata('home');

export default function Page() {
  return <StoryPage slug="home" />;
}
