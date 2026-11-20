import type { Blok } from '@/lib/types';
import { Heading, Img, Play, Section, src } from '@/components/ui/primitives';
import { Carousel, Tabs, VideoTrigger } from '@/components/ui/client';

/* -------------------------- Campus gallery ------------------------ */
function Mosaic({ images }: { images: any[] }) {
  const [first, ...rest] = images;
  return (
    <div className="grid grid-cols-2 gap-3 lg:grid-cols-4 lg:grid-rows-2">
      {first && (
        <div className="col-span-2 row-span-2 overflow-hidden rounded-2xl">
          <Img asset={first} className="aspect-[4/3] h-full w-full object-cover lg:aspect-auto" />
        </div>
      )}
      {rest.slice(0, 4).map((im, i) => (
        <div key={i} className="overflow-hidden rounded-2xl">
          <Img asset={im} className="aspect-[4/3] h-full w-full object-cover" />
        </div>
      ))}
    </div>
  );
}

export function CampusGallery({ blok }: { blok: Blok }) {
  const tabs: Blok[] = blok.tabs ?? [];
  return (
    <Section blok={blok} className="py-14 sm:py-20" tone="muted">
      <div className="wrap">
        <Heading eyebrow={blok.eyebrow} headline={blok.headline} muted={blok.muted} sub={blok.subhead} />
        <div className="mt-8">
          {tabs.length > 1 ? (
            <Tabs labels={tabs.map((t) => t.label)} panels={tabs.map((t) => <Mosaic key={t._uid} images={t.images ?? []} />)} />
          ) : (
            tabs[0] && <Mosaic images={tabs[0].images ?? []} />
          )}
        </div>
        {src(blok.video) && (
          <div className="mt-6">
            <VideoTrigger video={src(blok.video)}>
              <div className="relative aspect-[21/9] overflow-hidden rounded-2xl bg-night">
                <Img asset={blok.video_poster} className="h-full w-full object-cover transition duration-500 group-hover:scale-[1.02]" />
                <div className="absolute inset-0 bg-black/30" />
                <span className="absolute inset-0 flex items-center justify-center gap-3 text-white">
                  <span className="grid h-14 w-14 place-items-center rounded-full bg-white text-ink">
                    <Play className="ml-0.5 h-5 w-5" />
                  </span>
                  <span className="text-[16px] font-semibold">{blok.video_label}</span>
                </span>
              </div>
            </VideoTrigger>
          </div>
        )}
      </div>
    </Section>
  );
}

/* --------------------------- Sessions ----------------------------- */
export function Sessions({ blok }: { blok: Blok }) {
  return (
    <Section blok={blok} className="py-14 sm:py-20">
      <div className="wrap">
        <Heading eyebrow={blok.eyebrow} headline={blok.headline} muted={blok.muted} sub={blok.subhead} />
        <div className="mt-10">
          <Carousel label={blok.headline} itemClass="w-[82%] sm:w-[46%] lg:w-[31%]">
            {(blok.items ?? []).map((s: Blok) => (
              <article key={s._uid} className="card h-full overflow-hidden">
                <VideoTrigger video={s.video_url}>
                  <div className="relative aspect-video overflow-hidden bg-night">
                    <Img asset={s.image} className="h-full w-full object-cover transition duration-500 group-hover:scale-[1.03]" />
                    {s.video_url && (
                      <span className="absolute inset-0 grid place-items-center">
                        <span className="grid h-12 w-12 place-items-center rounded-full bg-white/95 text-ink shadow-lg">
                          <Play className="ml-0.5 h-5 w-5" />
                        </span>
                      </span>
                    )}
                  </div>
                </VideoTrigger>
                <div className="p-5">
                  <p className="text-[16px] font-semibold">{s.name}</p>
                  <p className="text-[12px] text-ink-4">{s.role}</p>
                  <p className="mt-3 text-[14px] leading-relaxed text-ink-3">{s.text}</p>
                  {src(s.logo) && <Img asset={s.logo} className="mt-4 h-5 w-auto" />}
                </div>
              </article>
            ))}
          </Carousel>
        </div>
      </div>
    </Section>
  );
}

/* -------------------------- Testimonials -------------------------- */
export function Testimonials({ blok }: { blok: Blok }) {
  return (
    <Section blok={blok} className="py-14 sm:py-20" tone="muted">
      <div className="wrap">
        <Heading eyebrow={blok.eyebrow} headline={blok.headline} muted={blok.muted} sub={blok.subhead} />
        <div className="mt-10">
          <Carousel label={blok.headline} itemClass="w-[62%] sm:w-[32%] lg:w-[19%]">
            {(blok.items ?? []).map((t: Blok) => (
              <VideoTrigger key={t._uid} video={t.video_url}>
                <figure className="overflow-hidden rounded-2xl bg-brand">
                  <div className="relative aspect-[3/4]">
                    <Img asset={t.image} alt={t.title} className="h-full w-full object-cover" />
                    {t.video_url && (
                      <span className="absolute inset-0 grid place-items-center">
                        <span className="grid h-11 w-11 place-items-center rounded-full bg-white/95 text-ink">
                          <Play className="ml-0.5 h-4 w-4" />
                        </span>
                      </span>
                    )}
                  </div>
                  {t.caption && <figcaption className="bg-white p-3 text-[13px] font-medium text-ink-2">{t.caption}</figcaption>}
                </figure>
              </VideoTrigger>
            ))}
          </Carousel>
        </div>
      </div>
    </Section>
  );
}
