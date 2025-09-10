import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SkaterOniceTable } from './skater-onice-table';

describe('SkaterOniceTable', () => {
  let component: SkaterOniceTable;
  let fixture: ComponentFixture<SkaterOniceTable>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SkaterOniceTable]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SkaterOniceTable);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
