import { Component, inject, input } from '@angular/core';
import { Router } from '@angular/router';
import { SkaterLeaderboardItem } from '../skater-leaderboard-item.model';
import { TableSortService } from '../../shared/table-sort.service';
import { DecimalPipe } from '@angular/common';
import { PositionPipe } from '../../pipes/position.pipe';

@Component({
  selector: 'app-shooting-table',
  imports: [DecimalPipe, PositionPipe],
  templateUrl: './shooting-table.html',
  styleUrl: './shooting-table.css'
})
export class ShootingTable {
  private router = inject(Router)
  sortService = inject(TableSortService)

  skaters = input.required<SkaterLeaderboardItem[]>();

  navigateToPlayer(id: number) {
    this.router.navigate(['players', id]);
  }
}
