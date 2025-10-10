import { Component, computed, input, signal } from '@angular/core';
import { SkaterLeaderboardItem } from '../skater-leaderboard-item.model';
import { timeOnIcePipe } from '../../pipes/timeOnIce.pipe';

@Component({
  selector: 'app-skater-table',
  imports: [timeOnIcePipe],
  templateUrl: './skater-table.html',
  styleUrl: './skater-table.css'
})
export class SkaterTable {
  skaters = input.required<SkaterLeaderboardItem[]>();
  itemsPerPage = input<number>(20);
  private currPage = signal<number>(0)
  private maxPages = computed<number>(() => Math.ceil(this.skaters().length / this.itemsPerPage()));
  skatersPage = computed<SkaterLeaderboardItem[]>(() => this.skaters().slice(this.currPage() * this.itemsPerPage(), (this.currPage() + 1) * this.itemsPerPage()))

  nextPage() {
    this.currPage.set(Math.min(this.currPage() + 1, this.maxPages() - 1));
  }

  prevPage() {
      this.currPage.set(Math.max(this.currPage() - 1, 0));
  }

  firstPage() {
      this.currPage.set(0);
  }

  lastPage() {
      this.currPage.set(this.maxPages() - 1);
  }
}
