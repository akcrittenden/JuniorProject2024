//This is our stores file for the allergens

import { writable } from 'svelte/store';
import { get } from 'svelte/store';

export const allergen = writable("");
export const severity = writable("mild");
export const allergens = writable<Allergen[]>([]);

// // Function to add allergens
// export function addAllergen(allergen, severity) {
//   if (allergen.trim() === "") {
//     alert("Please enter allergen.");
//     return;
//   }
  
//   allergens.update((currentAllergens) => {
//     // Checks if allergen is already in list
//     if (currentAllergens.find(item => item.allergen === allergen)) {
//       alert("Allergen already in your list.");
//       return currentAllergens; 
//     }
//     // Updates the allergen array with the new allergen
//     return [...currentAllergens, { allergen, severity }];
//   })
// }

// // Function to remove allergens
// export function removeAllergen(banish_allergen) {
//   allergens.update((currentAllergens) =>
//     currentAllergens.filter(item => item !== banish_allergen)
//   );
// }

interface Allergen {
  allergen: string;
  severity: string;
}

export function addAllergen(allergen: string, severity: string): void {
    if (allergen.trim() === "") {
      alert("Please enter allergen.");
      return;
    }
    const currentAllergens = get(allergens);
    if (currentAllergens.find(item => item.allergen === allergen)) {
      alert("Allergen already in your list.");
      return;
    }
  allergens.update((list: Allergen[]) => [...list, { allergen, severity }]);
}

export function removeAllergen(item: Allergen): void {
  allergens.update((list: Allergen[]) => list.filter((i: Allergen) => i !== item));
}

export function updateAllergen(index: number, newAllergen: string, newSeverity: string) {
  allergens.update((list: Allergen[]) => {
    console.log('Current list: ', list);
    const updatedList: Allergen[] = [...list];
    updatedList[index] = { allergen: newAllergen, severity: newSeverity };
    console.log('Updated list: ', updatedList);
    return updatedList;
  });
}
