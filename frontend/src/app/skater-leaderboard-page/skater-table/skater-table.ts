import { Component, inject, input } from '@angular/core';
import { SkaterLeaderboardItem } from '../skater-leaderboard-item.model';
import { timeOnIcePipe } from '../../pipes/timeOnIce.pipe';
import { Router } from '@angular/router';
import { TableSortService } from '../../shared/table-sort.service';
import { PositionPipe } from '../../pipes/position.pipe';

@Component({
  selector: 'app-skater-table',
  imports: [timeOnIcePipe, PositionPipe],
  templateUrl: './skater-table.html',
  styleUrl: './skater-table.css'
})
export class SkaterTable {
  private router = inject(Router)
  sortService = inject(TableSortService)

  skaters = input.required<SkaterLeaderboardItem[]>();

  navigateToPlayer(id: number) {
    this.router.navigate(['players', id]);
  }
}
