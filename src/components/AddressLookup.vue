<template>
  <div class="village-lookup">
    <!-- Province -->
    <label>Province</label>
    <select v-model="selectedProvince" @change="onProvinceChange">
      <option value="">-- Select Province --</option>
      <option
          v-for="pCode in provinceCodes"
          :key="pCode"
          :value="pCode"
      >
        {{ locations[pCode].name_kh }} / {{ locations[pCode].name_en }}
      </option>
    </select>

    <!-- District -->
    <label>District</label>
    <select v-model="selectedDistrict" @change="onDistrictChange">
      <option value="">-- Select District --</option>
      <option
          v-for="dCode in districtCodes"
          :key="dCode"
          :value="dCode"
      >
        {{ currentDistricts[dCode].name_kh }} / {{ currentDistricts[dCode].name_en }}
      </option>
    </select>

    <!-- Commune -->
    <label>Commune</label>
    <select v-model="selectedCommune" @change="onCommuneChange">
      <option value="">-- Select Commune --</option>
      <option
          v-for="cCode in communeCodes"
          :key="cCode"
          :value="cCode"
      >
        {{ currentCommunes[cCode].name_kh }} / {{ currentCommunes[cCode].name_en }}
      </option>
    </select>

    <!-- Village -->
    <label>Village</label>
    <select v-model="selectedVillage" @change="onVillageChange">
      <option value="">-- Select Village --</option>
      <option
          v-for="vCode in villageCodes"
          :key="vCode"
          :value="vCode"
      >
        {{ currentVillages[vCode].name_kh }} / {{ currentVillages[vCode].name_en }}
      </option>
    </select>
    <div>
      {{ addressKhmer }}
      <button v-if="addressKhmer"  @click="copyKhmerToClipboard">
        Copy
      </button>
    </div>
    <div>
      {{ addressEnglish }}
      <button v-if="addressEnglish" @click="copyEnglishToClipboard">
        Copy
      </button>
    </div>
  </div>
</template>

<script setup>
import {ref, computed, onMounted} from "vue";
import locationsJson from "@/assets/address.json";

const locations = ref({});
const selectedProvince = ref("");
const selectedDistrict = ref("");
const selectedCommune = ref("");
const selectedVillage = ref("");
let addressKhmer = ref("");
let addressEnglish = ref("");

// Load JSON on mount
onMounted(() => {
  locations.value = locationsJson;
});

// Province codes
const provinceCodes = computed(() => Object.keys(locations.value));

// Districts of selected province
const currentDistricts = computed(() => {
  if (!selectedProvince.value) return {};
  return locations.value[selectedProvince.value].districts || {};
});
const districtCodes = computed(() => Object.keys(currentDistricts.value));

// Communes of selected district
const currentCommunes = computed(() => {
  if (!selectedDistrict.value) return {};
  return currentDistricts.value[selectedDistrict.value].communes || {};
});
const communeCodes = computed(() => Object.keys(currentCommunes.value));

// Villages of selected commune
const currentVillages = computed(() => {
  if (!selectedCommune.value) return {};
  return currentCommunes.value[selectedCommune.value].villages || {};
});
const villageCodes = computed(() => Object.keys(currentVillages.value));

// Reset lower levels when upper changes
function onProvinceChange() {
  selectedDistrict.value = "";
  selectedCommune.value = "";
  selectedVillage.value = "";
}

function onDistrictChange() {
  selectedCommune.value = "";
  selectedVillage.value = "";
}

function onCommuneChange() {
  selectedVillage.value = "";
}

function onVillageChange() {
  if (parseInt(selectedProvince.value) === 12) {
    addressKhmer = `ភូមិ${currentVillages.value[selectedVillage.value].name_kh} សង្កាត់${currentCommunes.value[selectedCommune.value].name_kh}, ខណ្ឌ${currentDistricts.value[selectedDistrict.value].name_kh} ${locations.value[selectedProvince.value].name_kh}`;
    addressEnglish = `${currentVillages.value[selectedVillage.value].name_en} Village, Sangkat ${currentCommunes.value[selectedCommune.value].name_en}, Khan ${currentDistricts.value[selectedDistrict.value].name_en}, ${locations.value[selectedProvince.value].name_en} City`;
  } else {
    addressKhmer = `ភូមិ${currentVillages.value[selectedVillage.value].name_kh} ឃុំ${currentCommunes.value[selectedCommune.value].name_kh}, ស្រុក${currentDistricts.value[selectedDistrict.value].name_kh} ខេត្ត${locations.value[selectedProvince.value].name_kh}`;
    addressEnglish = `${currentVillages.value[selectedVillage.value].name_en} Village, ${currentCommunes.value[selectedCommune.value].name_en} Commune, ${currentDistricts.value[selectedDistrict.value].name_en} District, ${locations.value[selectedProvince.value].name_en} Province`;
  }
}

// Copy selected Khmer + English to clipboard
function copyEnglishToClipboard() {
  navigator.clipboard.writeText(addressEnglish)
      .then(() => alert("Copied"))
      .catch(err => alert("Failed to copy"));
}

function copyKhmerToClipboard() {
  navigator.clipboard.writeText(addressEnglish)
      .then(() => alert("Copied"))
      .catch(err => alert("Failed to copy"));
}
</script>

<style>
.village-lookup select {
  display: block;
  margin-bottom: 10px;
  padding: 5px;
}

.copy-section {
  margin-top: 15px;
}

.copy-section button {
  padding: 5px 10px;
  cursor: pointer;
}
</style>
