import { Component, computed, effect, inject, input, OnInit } from '@angular/core';
import { Award } from '../award.model';

import { GoalieStats } from '../goalie-stats.model';
import { SeasonPipe } from "../../pipes/season.pipe";
import { AwardBadge } from "../skater-totals-table/award-badge/award-badge";
import { BoldRecordPipe } from '../../pipes/bold-record.pipe';
import { SortConfig, TableSortService } from '../../shared/table-sort.service';

@Component({
  selector: 'app-goalie-totals-table',
  imports: [SeasonPipe, BoldRecordPipe, AwardBadge],
  templateUrl: './goalie-totals-table.html',
  styleUrl: './goalie-totals-table.css',
  providers: [TableSortService]
})
export class GoalieTotalsTable implements OnInit {
  sortService = inject(TableSortService<GoalieStats>);

  seasonStats = input.required<GoalieStats[]>();
  awards = input<Award[]>([]);

  statsEffect = effect(() => {
    this.sortService.setData(this.seasonStats())
  })

  stats = computed<GoalieStats[]>(() => this.sortService.sortedData())

  getSeasonAwards(season: number) {
    let seasonAwards = this.awards().filter((award) => {
      return award.season == season;
    }).map((award) => award.awardName)
    return seasonAwards
  }

  ngOnInit(): void {
    const sortConfig: SortConfig<GoalieStats> = {
      season: (item) => item.season,
      gamesPlayed: (item) => item.totals.gamesPlayed,
      gamesStarted: (item) => item.totals.gamesStarted,
      wins: (item) => item.totals.wins,
      losses: (item) => item.totals.losses,
      goalsAgainstAvg: (item) => item.totals.goalsAgainstAvg,
      savePct: (item) => item.totals.savePct ?? 0
    }

    this.sortService.setSortConfig(sortConfig);
  }
}
