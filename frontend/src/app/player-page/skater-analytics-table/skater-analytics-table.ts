import { Component, computed, effect, inject, input, OnInit } from '@angular/core';
import { SeasonPipe } from '../../pipes/season.pipe';
import { DecimalPipe } from '@angular/common';
import { SkaterStats } from '../skater-stats.model';
import { TableSortService, SortConfig } from '../../shared/table-sort.service';

@Component({
  selector: 'app-skater-analytics-table',
  imports: [SeasonPipe, DecimalPipe],
  templateUrl: './skater-analytics-table.html',
  styleUrl: './skater-analytics-table.css',
  providers: [TableSortService]
})
export class SkaterAnalyticsTable implements OnInit {
  sortService = inject(TableSortService<SkaterStats>);

  seasonStats = input.required<SkaterStats[]>();

  statsEffect = effect(() => {
    this.sortService.setData(this.seasonStats());
  })
  stats = computed<SkaterStats[]>(() => this.sortService.sortedData())

  ngOnInit(): void {
    const sortConfig: SortConfig<SkaterStats> = {
      season: (item) => item.season,
      gamesPlayed: (item) => item.totals.gamesPlayed,
      goalsAx: (item) => item.shooting.xgGoals - item.shooting.xg,
      shootingPct: (item) => item.totals.sog === 0 ? 0 : item.totals.goals / item.totals.sog,
      deltaFenwick: (item) => (item.shooting.xgGoals - item.shooting.xg) / item.shooting.fenwick
    }

    this.sortService.setSortConfig(sortConfig);
  }
}
