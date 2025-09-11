import { Component, computed, input } from '@angular/core';
import { SeasonPipe } from '../../pipes/season.pipe';
import { DecimalPipe } from '@angular/common';
import { SkaterStats } from '../skater-stats.model';

@Component({
  selector: 'app-skater-analytics-table',
  imports: [SeasonPipe, DecimalPipe],
  templateUrl: './skater-analytics-table.html',
  styleUrl: './skater-analytics-table.css'
})
export class SkaterAnalyticsTable {
  seasonStats = input.required<SkaterStats[]>();
}
