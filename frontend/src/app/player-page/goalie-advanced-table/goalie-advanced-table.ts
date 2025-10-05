import { Component, computed, effect, inject, input, OnInit } from '@angular/core';
import { GoalieStats } from '../goalie-stats.model';
import { SeasonPipe } from '../../pipes/season.pipe';
import { DecimalPipe } from '@angular/common';
import { TableSortService, SortConfig } from '../../shared/table-sort.service';

@Component({
  selector: 'app-goalie-advanced-table',
  imports: [SeasonPipe, DecimalPipe],
  templateUrl: './goalie-advanced-table.html',
  styleUrl: './goalie-advanced-table.css',
  providers: [TableSortService]
})
export class GoalieAdvancedTable implements OnInit {
  sortService = inject(TableSortService<GoalieStats>);
  
  seasonStats = input.required<GoalieStats[]>();

  statsEffect = effect(() => {
    this.sortService.setData(this.seasonStats())
  })

  stats = computed<GoalieStats[]>(() => this.sortService.sortedData())

  ngOnInit(): void {
    const sortConfig: SortConfig<GoalieStats> = {
      season: (item) => item.season,
      gamesPlayed: (item) => item.totals.gamesPlayed,
      goalsSavedAx: (item) => item.advanced.xgAgainst - item.advanced.xgGoalsAgainst,
      deltaFenwick: (item) => (item.advanced.xgAgainst - item.advanced.xgGoalsAgainst) / item.advanced.fenwickAgainst,
      evSavePct: (item) => item.totals.evenStrengthSavePct ?? 0,
      ppSavePct: (item) => item.totals.powerPlaySavePct ?? 0
    }

    this.sortService.setSortConfig(sortConfig);
  }

}
