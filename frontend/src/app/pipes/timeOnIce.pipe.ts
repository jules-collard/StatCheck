import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'timeOnIce',
  standalone: true
})
export class timeOnIcePipe implements PipeTransform {

  transform(value: number): string {
    const minutes = Math.floor(value / 60)
    const seconds = String(Math.round(value - minutes * 60)).padStart(2, '0')
    return `${minutes}:${seconds}`
  }
}
