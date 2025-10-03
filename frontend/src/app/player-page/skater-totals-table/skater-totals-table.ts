import { Component, computed, input, signal } from '@angular/core';
import { SkaterStats } from '../skater-stats.model';
import { SeasonPipe } from '../../pipes/season.pipe';
import { AwardBadge } from './award-badge/award-badge';
import { Award } from '../award.model';

import { timeOnIcePipe } from '../../pipes/timeOnIce.pipe';
import { BoldRecordPipe } from '../../pipes/bold-record.pipe';

@Component({
  selector: 'app-skater-totals-table',
  imports: [SeasonPipe, timeOnIcePipe, BoldRecordPipe, AwardBadge],
  templateUrl: './skater-totals-table.html',
  styleUrl: './skater-totals-table.css'
})
export class SkaterTotalsTable {
  seasonStats = input.required<SkaterStats[]>();
  awards = input<Award[]>([]);

  sortSeasons = signal<'asc'|'desc'|null>('asc');

  stats = computed<SkaterStats[]>(() => {
    if (this.sortSeasons() === 'asc') {
      return this.seasonStats().sort((a,b) => a.season - b.season);
    } else if (this.sortSeasons() === 'desc') {
      return this.seasonStats().sort((a,b) => b.season - a.season);
    }
    return this.seasonStats();
  })

  toggleSort(currentVal: 'asc'|'desc'|null) {
    if (currentVal === 'desc') {
        return 'asc';
    } else {
      return 'desc';
    }
  }

  getSeasonAwards(season: number) {
    let seasonAwards = this.awards().filter((award) => {
      return award.season == season;
    }).map((award) => award.awardName)
    return seasonAwards
  }
}
