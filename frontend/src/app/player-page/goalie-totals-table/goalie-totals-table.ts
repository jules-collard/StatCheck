import { Component, input } from '@angular/core';
import { Award } from '../award.model';

import { GoalieStats } from '../goalie-stats.model';
import { SeasonPipe } from "../../pipes/season.pipe";
import { AwardBadge } from "../season-totals-table/award-badge/award-badge";
import { DecimalPipe } from '@angular/common';
import { BoldRecordPipe } from '../../pipes/bold-record.pipe';

@Component({
  selector: 'app-goalie-totals-table',
  imports: [SeasonPipe, DecimalPipe, BoldRecordPipe, AwardBadge],
  templateUrl: './goalie-totals-table.html',
  styleUrl: './goalie-totals-table.css'
})
export class GoalieTotalsTable {
  seasonStats = input.required<GoalieStats[]>();
  awards = input<Award[]>([]);

  getSeasonAwards(season: number) {
    let seasonAwards = this.awards().filter((award) => {
      return award.season == season;
    }).map((award) => award.awardName)
    return seasonAwards
  }
}
