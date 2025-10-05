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
    console.log('Sending Data: ', this.seasonStats()[0])
    this.sortService.setData(this.seasonStats())
  })

  stats = computed<GoalieStats[]>(() => {
    const data = this.sortService.sortedData();
    console.log('Component: ', data[0]);
    return data;
  })

  getSeasonAwards(season: number) {
    let seasonAwards = this.awards().filter((award) => {
      return award.season == season;
    }).map((award) => award.awardName)
    return seasonAwards
  }

  ngOnInit(): void {
    const sortConfig: SortConfig<GoalieStats> = {
      season: (item) => item.season
    }

    this.sortService.setSortConfig(sortConfig);
  }
}
