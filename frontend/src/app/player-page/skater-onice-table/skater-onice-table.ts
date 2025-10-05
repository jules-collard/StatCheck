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
      season: (item) => item.season
    }

    this.sortService.setSortConfig(sortConfig);
  }
}
