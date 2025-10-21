import { Component, inject, input } from '@angular/core';
import { TableSortService } from '../../shared/table-sort.service';
import { Router } from '@angular/router';
import { GoalieLeaderboardItem } from '../goalie-leaderboard-item.model';
import { DecimalPipe } from '@angular/common';

@Component({
  selector: 'app-goalie-table',
  imports: [DecimalPipe],
  templateUrl: './goalie-table.html',
  styleUrl: './goalie-table.css'
})
export class GoalieTable {
  private router = inject(Router)
  sortService = inject(TableSortService)

  goalies = input.required<GoalieLeaderboardItem[]>();

  navigateToPlayer(id: number) {
    this.router.navigate(['players', id]);
  }
}
