import { Component, input } from '@angular/core';
import { SeasonTotals } from '../player-season-totals/season-totals.model';
import { SeasonPipe } from '../../pipes/season.pipe';
import { AwardBadge } from '../player-season-totals/award-badge/award-badge';
import { Award } from '../award.model';

@Component({
  selector: 'app-season-totals-table',
  imports: [SeasonPipe, AwardBadge],
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
