//This is our stores file for the allergens

import { writable } from 'svelte/store';
export const allergen = writable("");
export const severity = writable("mild");
export const allergens = writable([]);

// Function to add allergens
export function addAllergen(allergen, severity) {
  if (allergen.trim() === "") {
    alert("Please enter allergen.");
    return;
  }
  
  allergens.update((currentAllergens) => {
    // Checks if allergen is already in list
    if (currentAllergens.find(item => item.allergen === allergen)) {
      alert("Allergen already in your list.");
      return currentAllergens; 
    }
    // Updates the allergen array with the new allergen
    return [...currentAllergens, { allergen, severity }];
  })
}

// Function to remove allergens
export function removeAllergen(banish_allergen) {
  allergens.update((currentAllergens) =>
    currentAllergens.filter(item => item !== banish_allergen)
  );
}