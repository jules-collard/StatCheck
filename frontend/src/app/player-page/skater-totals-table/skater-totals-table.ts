import { Component, computed, input, signal } from '@angular/core';
import { SkaterStats } from '../skater-stats.model';
import { SeasonPipe } from '../../pipes/season.pipe';
import { AwardBadge } from './award-badge/award-badge';
import { Award } from '../award.model';

import { timeOnIcePipe } from '../../pipes/timeOnIce.pipe';
import { BoldRecordPipe } from '../../pipes/bold-record.pipe';
import { form } from '@angular/forms/signals';

@Component({
  selector: 'app-skater-totals-table',
  imports: [SeasonPipe, timeOnIcePipe, BoldRecordPipe, AwardBadge],
  templateUrl: './skater-totals-table.html',
  styleUrl: './skater-totals-table.css'
})
export class SkaterTotalsTable {
  seasonStats = input.required<SkaterStats[]>();
  awards = input<Award[]>([]);

  sorting = signal<{
    seasons: 'asc'|'desc'|null;
    gamesPlayed: 'asc'|'desc'|null;
  }>({
    seasons: 'asc',
    gamesPlayed: null
  });

  sortingForm = form(this.sorting)

  stats = computed<SkaterStats[]>(() => {
    if (this.sortingForm.seasons().value() === 'asc') {
      return this.seasonStats().sort((a,b) => a.season - b.season);
    } else if (this.sortingForm.seasons().value() === 'desc') {
      return this.seasonStats().sort((a,b) => b.season - a.season);
    }

    if (this.sortingForm.gamesPlayed().value() === 'asc') {
      return this.seasonStats().sort((a,b) => a.totals.gamesPlayed - b.totals.gamesPlayed);
    } else if (this.sortingForm.gamesPlayed().value() === 'desc') {
      return this.seasonStats().sort((a,b) => b.totals.gamesPlayed - a.totals.gamesPlayed);
    }
    return this.seasonStats();
  })

  toggleSort(currentVal: 'asc'|'desc'|null) {
    this.resetSorting();
    if (currentVal === 'desc') {
        return 'asc';
    } else {
      return 'desc';
    }
  }

  resetSorting() {
    this.sortingForm.seasons().value.set(null)
    this.sortingForm.gamesPlayed().value.set(null)
  }

  getSeasonAwards(season: number) {
    let seasonAwards = this.awards().filter((award) => {
      return award.season == season;
    }).map((award) => award.awardName)
    return seasonAwards
  }
}
