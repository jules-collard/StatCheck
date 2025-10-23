import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SkaterTable } from './skater-table';

describe('SkaterTable', () => {
  let component: SkaterTable;
  let fixture: ComponentFixture<SkaterTable>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SkaterTable]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SkaterTable);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
