import { Component, computed, input, signal } from '@angular/core';
import { SkaterLeaderboardItem } from '../skater-leaderboard-item.model';
import { timeOnIcePipe } from '../../pipes/timeOnIce.pipe';

@Component({
  selector: 'app-skater-table',
  imports: [timeOnIcePipe],
  templateUrl: './skater-table.html',
  styleUrl: './skater-table.css'
})
export class SkaterTable {
  skaters = input.required<SkaterLeaderboardItem[]>();
}
