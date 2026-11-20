import StoryPage, { storyMetadata } from '@/components/site/StoryPage';
import { localStories } from '@/content';

// Any Storyblok story renders at /<its slug>, so editors can add pages
// (e.g. /scholarships) in Storyblok without a code change.
export const revalidate = 60;
export const dynamicParams = true;

const HIDDEN = new Set(['home', 'config']);

export function generateStaticParams() {
  return Object.keys(localStories)
    .filter((s) => !HIDDEN.has(s))
    .map((s) => ({ slug: s.split('/') }));
}

type Props = { params: Promise<{ slug: string[] }> };

export async function generateMetadata({ params }: Props) {
  const { slug } = await params;
  return storyMetadata(slug.join('/'));
}

export default async function Page({ params }: Props) {
  const { slug } = await params;
  const path = slug.join('/');
  return <StoryPage slug={HIDDEN.has(path) ? '__none__' : path} />;
}
