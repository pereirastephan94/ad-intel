// Every section on the site is a Storyblok "blok": an object with a `component`
// name, a unique `_uid`, and its own fields. Local content in /content uses the
// exact same shape, so the site renders identically from either source.

export type Asset = { filename: string; alt?: string };

export type Blok = {
  component: string;
  _uid: string;
  _editable?: string;
  [field: string]: any;
};

export type StoryContent = Blok & {
  body?: Blok[];
  seo_title?: string;
  seo_description?: string;
};

export type Story = {
  name: string;
  slug: string;
  full_slug: string;
  content: StoryContent;
};
