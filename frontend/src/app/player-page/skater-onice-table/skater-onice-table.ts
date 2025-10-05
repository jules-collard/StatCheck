import { Component, computed, effect, inject, input, OnInit } from '@angular/core';
import { SkaterStats } from '../skater-stats.model';
import { SeasonPipe } from '../../pipes/season.pipe';
import { DecimalPipe } from '@angular/common';
import { SortConfig, TableSortService } from '../../shared/table-sort.service';

@Component({
  selector: 'app-skater-onice-table',
  imports: [SeasonPipe, DecimalPipe],
  templateUrl: './skater-onice-table.html',
  styleUrl: './skater-onice-table.css',
  providers: [TableSortService]
})
export class SkaterOnIceTable implements OnInit {
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
      corsiFor: (item) => item.onIce.corsiFor / (item.onIce.corsiFor + item.onIce.corsiAgainst),
      fenwickFor: (item) => item.onIce.fenwickFor / (item.onIce.fenwickFor + item.onIce.fenwickAgainst),
      xgFor: (item) => item.onIce.xgFor / (item.onIce.xgFor + item.onIce.xgAgainst),
      onIceShootingPct: (item) => item.onIce.onIceShootingPct,
      oZoneStarts: (item) => item.onIce.oZoneStarts / (item.onIce.oZoneStarts + item.onIce.nZoneStarts + item.onIce.dZoneStarts),
      dZoneStarts: (item) => item.onIce.dZoneStarts / (item.onIce.oZoneStarts + item.onIce.nZoneStarts + item.onIce.dZoneStarts)
    }

    this.sortService.setSortConfig(sortConfig);
  }
}
