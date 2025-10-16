import { Component, computed, inject, input, signal } from '@angular/core';
import { SkaterLeaderboardItem } from '../skater-leaderboard-item.model';
import { timeOnIcePipe } from '../../pipes/timeOnIce.pipe';
import { Router } from '@angular/router';

@Component({
  selector: 'app-skater-table',
  imports: [timeOnIcePipe],
  templateUrl: './skater-table.html',
  styleUrl: './skater-table.css'
})
export class SkaterTable {
  private router = inject(Router)

  skaters = input.required<SkaterLeaderboardItem[]>();

  navigateToPlayer(id: number) {
    this.router.navigate(['players', id])
  }
}
