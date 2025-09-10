import { Component, input } from '@angular/core';
import { GoalieStats } from '../goalie-stats.model';
import { SeasonPipe } from '../../pipes/season.pipe';
import { DecimalPipe } from '@angular/common';

@Component({
  selector: 'app-goalie-advanced-table',
  imports: [SeasonPipe, DecimalPipe],
  templateUrl: './goalie-advanced-table.html',
  styleUrl: './goalie-advanced-table.css'
})
export class GoalieAdvancedTable {
  seasonStats = input.required<GoalieStats[]>()
}
