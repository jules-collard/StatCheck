import { Injectable, signal, computed, linkedSignal } from "@angular/core";

export type SortDirection = 'asc' | 'desc' | null;

export interface SortConfig<T> {
    [key: string]: (item: T) => number;
}

@Injectable()
export class TableSortService<T> {
    private sortState = signal<{column: string | null, direction: SortDirection}>({
        column: null,
        direction: null
    })

    private sortConfig = signal<SortConfig<T> | null>(null);
    private data = signal<T[]>([]);
    
    setSortConfig(config: SortConfig<T>) {
        this.sortConfig.set(config);
    }

    setData(data: T[]) {
        this.data.set(data)
    }

    sortedData = linkedSignal<T[]>(() => this.data())

    toggleSort(column: string) {
        if (!this.sortConfig()) {
            return;
        } else if (this.sortState().column === column) {
            // Cycle through null -> desc -> asc -> desc
            if (this.sortState().direction === 'desc') {
                this.sortState.update((state) => ({...state, direction: 'asc'}));
            } else if (this.sortState().direction === 'asc') {
                this.sortState.update((state) => ({...state, direction: 'desc'}));
            } else {
                this.sortState.update((state) => ({...state, direction: 'desc'}));
            }
        } else {
            this.sortState.set({column: column, direction: 'desc'})
        }

        this.sortedData.update((data) => {
            const getValue = this.sortConfig()![this.sortState().column!];
            if (!getValue) {
                return [...data];
            } else {
                return [...data].sort((a,b) => {
                    const valueA = getValue(a);
                    const valueB = getValue(b);

                    if (this.sortState().direction === 'asc') {
                        return valueA - valueB;
                    } else {
                        return valueB - valueA;
                    }
                })
            }
        })
    }

    getSortIcon(column: string): string {
        const direction = this.sortState().column === column ? this.sortState().direction : null;
        switch (direction) {
            case 'asc': return '↑';
            case 'desc': return '↓';
            default: return '';
        }
    }

    reset() {
        this.sortState.set({column: null, direction: null});
    }
}