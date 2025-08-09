import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'season',
  standalone: true
})
export class SeasonPipe implements PipeTransform {

  transform(value: number) {
    var season = value.toString();
    const firstYear = season.slice(0, 4);
    const secondYear = season.slice(4);
    return firstYear + '-' + secondYear;
  }
}
