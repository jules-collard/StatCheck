import { Component, input } from '@angular/core';
import { SeasonTotals } from './season-totals.model';
import { SeasonPipe } from '../../pipes/season.pipe';
import { AwardBadge } from './award-badge/award-badge';
import { Award } from '../award.model';
import { timeOnIcePipe } from '../../pipes/timeOnIce.pipe';

@Component({
  selector: 'app-season-totals-table',
  imports: [SeasonPipe, timeOnIcePipe, AwardBadge],
  templateUrl: './season-totals-table.html',
  styleUrl: './season-totals-table.css'
})
export class SeasonTotalsTable {
  seasonTotals = input.required<SeasonTotals[]>();
  awards = input<Award[]>([]);

  getSeasonAwards(season: number) {
    let seasonAwards = this.awards().filter((award) => {
      return award.season == season;
    }).map((award) => award.awardName)
    return seasonAwards
  }
}
