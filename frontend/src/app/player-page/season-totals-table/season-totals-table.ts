import { Component, computed, input } from '@angular/core';
import { SkaterStats } from '../skater-stats.model';
import { SeasonPipe } from '../../pipes/season.pipe';
import { AwardBadge } from './award-badge/award-badge';
import { Award } from '../award.model';

import { timeOnIcePipe } from '../../pipes/timeOnIce.pipe';
import { BoldRecordPipe } from '../../pipes/bold-record.pipe';

@Component({
  selector: 'app-season-totals-table',
  imports: [SeasonPipe, timeOnIcePipe, BoldRecordPipe, AwardBadge],
  templateUrl: './season-totals-table.html',
  styleUrl: './season-totals-table.css'
})
export class SeasonTotalsTable {
  seasonStats = input.required<SkaterStats[]>();
  awards = input<Award[]>([]);

  getSeasonAwards(season: number) {
    let seasonAwards = this.awards().filter((award) => {
      return award.season == season;
    }).map((award) => award.awardName)
    return seasonAwards
  }
}
