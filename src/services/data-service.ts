import { ref } from "vue";

export interface Donor {
  name: string;
  amount?: number;
}

export interface WordCloudItem {
  text: string;
  value: number;
}

export const topDonors = ref<Donor[]>([]);
export const latestDonations = ref<Donor[]>([]);
export const wordCloud = ref<WordCloudItem[]>([]);

export async function fetchData() {
  try {
    const basePath = import.meta.env.BASE_URL;
    const response = await fetch(`${basePath}donors.json`);
    const data = await response.json();

    topDonors.value = data.topDonors || [];
    latestDonations.value = data.latestDonations || [];
    wordCloud.value = data.wordCloud || [];
  } catch (error) {
    console.error("Failed to fetch donor data:", error);
    // Keep the app running with empty data
    topDonors.value = [];
    latestDonations.value = [];
    wordCloud.value = [];
  }
}
