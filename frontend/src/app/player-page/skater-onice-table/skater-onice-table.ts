import { Component, input } from '@angular/core';
import { SkaterStats } from '../skater-stats.model';
import { SeasonPipe } from '../../pipes/season.pipe';
import { DecimalPipe } from '@angular/common';

@Component({
  selector: 'app-skater-onice-table',
  imports: [SeasonPipe, DecimalPipe],
  templateUrl: './skater-onice-table.html',
  styleUrl: './skater-onice-table.css'
})
export class SkaterOnIceTable {
  seasonStats = input.required<SkaterStats[]>()
}
