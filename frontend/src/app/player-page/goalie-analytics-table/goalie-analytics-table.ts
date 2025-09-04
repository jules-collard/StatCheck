import { Component, input } from '@angular/core';
import { GoalieTotals } from '../goalie-totals-table/goalie-totals.model';
import { SeasonPipe } from '../../pipes/season.pipe';
import { DecimalPipe } from '@angular/common';

@Component({
  selector: 'app-goalie-analytics-table',
  imports: [SeasonPipe, DecimalPipe],
  templateUrl: './goalie-analytics-table.html',
  styleUrl: './goalie-analytics-table.css'
})
export class GoalieAnalyticsTable {
  seasonTotals = input.required<GoalieTotals[]>()
}
