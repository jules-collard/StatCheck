import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'position',
  standalone: true
})
export class PositionPipe implements PipeTransform {

  transform(value: "G" | "D" | "L" | "C" | "R") {
    if (value === "L" || value === "R") {
        return value + 'W'
    } else {
        return value
    }
  }
}