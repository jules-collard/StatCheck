import { Component, computed, effect, inject, input, OnInit } from '@angular/core';

import { SkaterStats } from '../skater-stats.model';
import { SeasonPipe } from '../../pipes/season.pipe';
import { AwardBadge } from './award-badge/award-badge';
import { Award } from '../award.model';
import { timeOnIcePipe } from '../../pipes/timeOnIce.pipe';
import { BoldRecordPipe } from '../../pipes/bold-record.pipe';
import { SortConfig, TableSortService } from '../../shared/table-sort.service';

@Component({
  selector: 'app-skater-totals-table',
  imports: [SeasonPipe, timeOnIcePipe, BoldRecordPipe, AwardBadge],
  templateUrl: './skater-totals-table.html',
  styleUrl: './skater-totals-table.css',
  providers: [TableSortService]
})
export class SkaterTotalsTable implements OnInit {
  sortService = inject(TableSortService<SkaterStats>);

  seasonStats = input.required<SkaterStats[]>();
  awards = input<Award[]>([]);

  statsEffect = effect(() => {
    this.sortService.setData(this.seasonStats());
  })

  stats = computed(() => this.sortService.sortedData());

  getSeasonAwards(season: number) {
    let seasonAwards = this.awards().filter((award) => {
      return award.season == season;
    }).map((award) => award.awardName)
    return seasonAwards;
  }

  ngOnInit(): void {
    const sortConfig: SortConfig<SkaterStats> = {
      season: (item) => item.season,
      gamesPlayed: (item) => item.totals.gamesPlayed,
      goals: (item) => item.totals.goals,
      assists: (item) => item.totals.assists,
      points: (item) => item.totals.goals + item.totals.assists,
      plusMinus: (item) => item.totals.plusMinus,
      sog: (item) => item.totals.sog,
      hits: (item) => item.totals.hits,
      blocks: (item) => item.totals.blocks,
      penaltyMinutes: (item) => item.totals.penaltyMinutes,
      avgTOI: (item) => item.totals.avgTOI
    }

    this.sortService.setSortConfig(sortConfig);
  }
}
