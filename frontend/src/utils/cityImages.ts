/**
 * Destination images served from /images/ (public/images/ symlinked or copied from data/).
 * Falls back gracefully to a placeholder if the image fails to load.
 */

export interface CityImageSet {
  cover: string;
  locations?: string[];
  food?: string[];
  shopping?: string[];
}

const BASE = "/images";

export const cityImages: Record<string, CityImageSet> = {
  bali: { cover: `${BASE}/bali/bali.jpg` },
  "cape-town": { cover: `${BASE}/cape-town/cape-town.jpg` },
  coimbatore: { cover: `${BASE}/coimbatore/coimbatore.jpg` },
  dubai: { cover: `${BASE}/dubai/dubai.jpg` },
  hampi: { cover: `${BASE}/hampi/hampi.jpg` },
  jaipur: { cover: `${BASE}/jaipur/cover-photo.jpg` },
  kyoto: { cover: `${BASE}/kyoto/kyoto.jpg` },
  nalanda: { cover: `${BASE}/nalanda/nalanda.jpg` },
  puducherry: { cover: `${BASE}/puducherry/puducherry.jpg` },
  "rio-de-janerio": { cover: `${BASE}/rio-de-janerio/rio-de-janerio.jpg` },
  rishikesh: { cover: `${BASE}/rishikesh/rishikesh.jpg` },
  santorini: { cover: `${BASE}/santorini/santorini.jpg` },
  seoul: { cover: `${BASE}/seoul/seoul.jpg` },
  shillong: { cover: `${BASE}/shillong/shillong.jpg` },
  singapore: {
    cover: `${BASE}/singapore/singapore.jpg`,
    locations: [
      `${BASE}/singapore/locations/Gardens by the Bay.jpg`,
      `${BASE}/singapore/locations/Marina Bay Sands.jpg`,
      `${BASE}/singapore/locations/Sentosa Island.jpg`,
    ],
    food: [
      `${BASE}/singapore/food/Chili Crab.jpg`,
      `${BASE}/singapore/food/Laksa.jpg`,
      `${BASE}/singapore/food/Satay.jpg`,
    ],
    shopping: [
      `${BASE}/singapore/things-to-buy/Bak Kwa.jpg`,
      `${BASE}/singapore/things-to-buy/TWG Tea Products.jpg`,
    ],
  },
  sydney: {
    cover: `${BASE}/sydney/sydney.jpg`,
    locations: [
      `${BASE}/sydney/locations/Bondi Beach.jpg`,
      `${BASE}/sydney/locations/Sydney Harbour Bridge.jpg`,
      `${BASE}/sydney/locations/Sydney Opera House.jpg`,
    ],
    food: [
      `${BASE}/sydney/food/Fish and Chips.jpg`,
      `${BASE}/sydney/food/Barramundi.jpg`,
      `${BASE}/sydney/food/Avocado Toast and Brunch Specials.jpg`,
    ],
    shopping: [
      `${BASE}/sydney/things-to-buy/UGG Boots.jpg`,
      `${BASE}/sydney/things-to-buy/Opal Jewelry.jpg`,
    ],
  },
  varanasi: {
    cover: `${BASE}/varanasi/Varanasi.jpg`,
    locations: [
      `${BASE}/varanasi/locations/Dashashwamedh Ghat.jpg`,
      `${BASE}/varanasi/locations/Kashi Vishwanath Temple.jpg`,
      `${BASE}/varanasi/locations/Sarnath.jpg`,
    ],
    food: [
      `${BASE}/varanasi/food/lassi.jpg`,
      `${BASE}/varanasi/food/paan.jpg`,
      `${BASE}/varanasi/food/Tamatar Chaat.jpg`,
    ],
    shopping: [
      `${BASE}/varanasi/things-to-buy/Banarasi Silk Sarees.jpg`,
      `${BASE}/varanasi/things-to-buy/Rudraksha and Spiritual Items.jpg`,
    ],
  },
  venice: {
    cover: `${BASE}/venice/12019-venice-2451047.jpg`,
    locations: [
      `${BASE}/venice/locations/Grand Canal.jpg`,
      `${BASE}/venice/locations/Rialto Bridge.jpg`,
      `${BASE}/venice/locations/St. Mark's Basilica.jpg`,
    ],
    food: [
      `${BASE}/venice/food/Tiramisu.jpg`,
      `${BASE}/venice/food/Cicchetti.jpg`,
      `${BASE}/venice/food/Sarde in Saor.jpg`,
    ],
    shopping: [
      `${BASE}/venice/things-to-buy/venetian masks.jpg`,
      `${BASE}/venice/things-to-buy/Burano Lace.jpg`,
    ],
  },
};

/**
 * Rotating hero destinations for the landing page slideshow.
 * Ordered by visual impact.
 */
export const heroImages: Array<{ src: string; city: string; country: string }> = [
  { src: cityImages.santorini.cover, city: "Santorini", country: "Greece" },
  { src: cityImages.kyoto.cover, city: "Kyoto", country: "Japan" },
  { src: cityImages.bali.cover, city: "Bali", country: "Indonesia" },
  { src: cityImages.venice.cover, city: "Venice", country: "Italy" },
  { src: cityImages.dubai.cover, city: "Dubai", country: "UAE" },
  { src: cityImages.singapore.cover, city: "Singapore", country: "Singapore" },
  { src: cityImages.sydney.cover, city: "Sydney", country: "Australia" },
  { src: cityImages.seoul.cover, city: "Seoul", country: "South Korea" },
  { src: cityImages["rio-de-janerio"].cover, city: "Rio de Janeiro", country: "Brazil" },
  { src: cityImages.varanasi.cover, city: "Varanasi", country: "India" },
  { src: cityImages.jaipur.cover, city: "Jaipur", country: "India" },
  { src: cityImages.rishikesh.cover, city: "Rishikesh", country: "India" },
  { src: cityImages.shillong.cover, city: "Shillong", country: "India" },
  { src: cityImages.hampi.cover, city: "Hampi", country: "India" },
  { src: cityImages.nalanda.cover, city: "Nalanda", country: "India" },
  { src: cityImages.coimbatore.cover, city: "Coimbatore", country: "India" },
  { src: cityImages.puducherry.cover, city: "Puducherry", country: "India" },
  { src: cityImages["cape-town"].cover, city: "Cape Town", country: "South Africa" },
];

/**
 * Returns the local cover image path for a city slug.
 * Falls back to Santorini if the slug is not in the local set.
 */
export function getCityImage(slug: string): string {
  return cityImages[slug]?.cover ?? cityImages.santorini.cover;
}

/**
 * Returns a safe img onError handler that hides broken images gracefully.
 */
export function onImgError(e: React.SyntheticEvent<HTMLImageElement>) {
  const img = e.currentTarget;
  img.style.display = "none";
}
