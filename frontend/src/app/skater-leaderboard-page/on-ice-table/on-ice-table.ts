import { Component, inject, input } from '@angular/core';
import { Router } from '@angular/router';
import { SkaterLeaderboardItem } from '../skater-leaderboard-item.model';
import { TableSortService } from '../../shared/table-sort.service';
import { PositionPipe } from '../../pipes/position.pipe';
import { DecimalPipe } from '@angular/common';

@Component({
  selector: 'app-on-ice-table',
  imports: [PositionPipe, DecimalPipe],
  templateUrl: './on-ice-table.html',
  styleUrl: './on-ice-table.css'
})
export class OnIceTable {
  private router = inject(Router)
  sortService = inject(TableSortService)

  skaters = input.required<SkaterLeaderboardItem[]>();

  navigateToPlayer(id: number) {
    this.router.navigate(['players', id]);
  }
}
