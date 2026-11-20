import { notFound } from 'next/navigation';
import type { Metadata } from 'next';
import { Blocks } from '@/components/bloks';
import { getStory } from '@/lib/storyblok';

export async function storyMetadata(slug: string): Promise<Metadata> {
  const story = await getStory(slug);
  if (!story) return {};
  return {
    title: story.content.seo_title || story.name,
    description: story.content.seo_description,
  };
}

export default async function StoryPage({ slug }: { slug: string }) {
  const story = await getStory(slug);
  if (!story) notFound();
  return <Blocks body={story.content.body} />;
}
