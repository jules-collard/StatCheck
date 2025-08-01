import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'height',
  standalone: true
})
export class HeightPipe implements PipeTransform {

  transform(value: number | null, unit: 'in' | 'cm') {
    if (value === null) { return 'Unknown' }
    else if (unit === 'in') {
      const feet = Math.floor(value / 12);
      const inches = value - (feet * 12);
      return `${feet}ft ${inches}in`;
    } else { // cm
      const meters = Math.floor(value / 100);
      const centimeters = value - (meters * 100);
      return `${meters}m ${centimeters}cm`;
    }
  }
}
