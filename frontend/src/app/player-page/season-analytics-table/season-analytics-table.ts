import { Component, computed, input } from '@angular/core';
import { SeasonPipe } from '../../pipes/season.pipe';
import { DecimalPipe } from '@angular/common';
import { SeasonTotals } from '../season-totals-table/season-totals.model';

@Component({
  selector: 'app-season-analytics-table',
  imports: [SeasonPipe, DecimalPipe],
  templateUrl: './season-analytics-table.html',
  styleUrl: './season-analytics-table.css'
})
export class SeasonAnalyticsTable {
  seasonTotals = input.required<SeasonTotals[]>();
}
