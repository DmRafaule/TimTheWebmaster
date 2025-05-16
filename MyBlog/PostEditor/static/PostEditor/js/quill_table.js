// Tables
// Table tooltip
class TableTooltip extends Quill.import('ui/tooltip'){
    constructor(scroll, domNode, placeholder = ''){
        let prev = document.querySelector('.table-tooltip')
        if (prev){
            prev.remove()
        }
        super(scroll, domNode);
        this.textbox = null
        this.root.innerText = ""
        this.root.classList.add('table-tooltip')
        this.insertBtn(`${PATH}PostEditor/img/table-insert-row-above.svg`, document.querySelector('#insertRowAbove_text').innerText, this.insertRowAbove)
        this.insertBtn(`${PATH}PostEditor/img/table-insert-row-after.svg`, document.querySelector('#insertRowBelow_text').innerText, this.insertRowBelow)
        this.insertBtn(`${PATH}PostEditor/img/table-insert-column-after.svg`, document.querySelector('#insertColumnAfter_text').innerText, this.insertColumnAfter)
        this.insertBtn(`${PATH}PostEditor/img/table-insert-column-before.svg`, document.querySelector('#insertColumnBefore_text').innerText, this.insertColumnBefore)
        this.insertSep()
        this.insertBtn(`${PATH}PostEditor/img/table-top-header.svg`, document.querySelector('#insertTopHeader_text').innerText, this.toggleHeader)
        this.insertSep()
        this.insertBtn(`${PATH}PostEditor/img/table-delete-row.svg`, document.querySelector('#removeRow_text').innerText, this.removeRow)
        this.insertBtn(`${PATH}PostEditor/img/table-delete-column.svg`, document.querySelector('#removeCol_text').innerText, this.removeCol)
        this.insertSep()
        this.insertBtn(`${PATH}PostEditor/img/table-delete.svg`, document.querySelector('#removeTable_text').innerText, this.removeTable)
        this.setHeight(document.querySelector('footer').getBoundingClientRect().height)
        document.querySelector('footer').classList.add('active')
    }

    insertSep(){
        let container = document.createElement('div')
        container.classList.add('el-expandable')
        this.root.insertAdjacentElement('beforeend', container)
    }

    insertBtn(iconPath, popupText, callback){
        let icon = document.createElement('img')
        icon.classList.add('icon')
        icon.classList.add('dynamic_image')
        icon.width = '32'
        icon.height = '32'
        icon.src = iconPath
        let container = document.createElement('div')
        container.classList.add('button')
        container.classList.add('squered_button')
        container.addEventListener('click', callback)
        container.insertAdjacentElement('beforeend', icon)
        let tip = document.createElement('abbr')
        tip.setAttribute('title', popupText)
        tip.insertAdjacentElement('beforeend', container)
        this.root.insertAdjacentElement('beforeend', tip)
    }

    insertRowAbove(event){
        const table = quill.getModule('table');
        table.insertRowAbove()
    }

    insertRowBelow(event){
        const table = quill.getModule('table');
        table.insertRowBelow()
    }

    insertColumnAfter(event){
        const table = quill.getModule('table');
        table.insertColumnRight()
    }

    insertColumnBefore(event){
        const table = quill.getModule('table');
        table.insertColumnLeft()
    }


    toggleHeader(event){
        const table = quill.getModule('table');
        const body = table.getTable()[0].children.tail
        if (body == null || body.domNode.nodeName != TableHeader.tagName)
            table.insertHeader()
        else
            table.deleteHeader()
    }

    removeRow(event){
        const table = quill.getModule('table');
        table.deleteRow()
    }

    removeCol(event){
        const table = quill.getModule('table');
        table.deleteColumn()
    }

    removeTable(event){
        const table = quill.getModule('table');
        table.deleteTable()
        TableTooltip.remove()
    }

    static remove(){
        let prev = document.querySelector('.table-tooltip')
        if (prev){
            prev.remove()
        }
        document.querySelector('footer').classList.remove('active')
    }

    cancel() {
        this.hide();
        this.restoreFocus();
    }

    restoreFocus() {
        this.quill.focus({ preventScroll: true });
    }
    setHeight(height){
        this.root.style.height = `${height}px`
    }

}

function tableId() {
    const id = Math.random().toString(36).slice(2, 6);
    return `row-${id}`;
}

class TableHeaderCell extends Quill.import('formats/table'){}
TableHeaderCell.blotName = 'table-head-cell';
TableHeaderCell.tagName = 'TH';

class MyTableRow extends Quill.import('formats/table-row') {}
MyTableRow.allowedChildren.push(TableHeaderCell)
TableHeaderCell.requiredContainer = MyTableRow

class TableHeader extends Quill.import('formats/table-body') {}
TableHeader.blotName = 'table-head';
TableHeader.tagName = 'THEAD';

class MyTableContainer extends Quill.import('formats/table-container') {

    insertHeaderRow() {
        const body = this.scroll.create(TableHeader.blotName);
        const id = tableId();
        const row = this.scroll.create(MyTableRow.blotName);
        body.appendChild(row)
        this.children.head.children.head.children.forEach(() => {
            const cell = this.scroll.create(TableHeaderCell.blotName, id);
            row.appendChild(cell);
        });
        this.appendChild(body)
    }

    insertHeaderColumn(index) {
        const body = this.children.tail
        if (body == null || body.children.head == null || body.domNode.nodeName != TableHeader.tagName) return;
        body.children.forEach((row) => {
          const ref = row.children.at(index);
          const value = TableHeaderCell.formats(row.children.head.domNode);
          const cell = this.scroll.create(TableHeaderCell.blotName, value);
          row.insertBefore(cell, ref);
        });
    }

    deleteHeaderRow() {
        const body = this.children.tail
        if (body == null || body.children.head == null || body.domNode.nodeName != TableHeader.tagName) return;
        body.remove()
    }

    deleteHeaderColumn(index) {
        const body = this.children.tail
        if (body == null || body.children.head == null || body.domNode.nodeName != TableHeader.tagName) return;
        body.children.forEach((row) => {
          const cell = row.children.at(index);
          if (cell != null) {
            cell.remove();
          }
        });
    }
}
MyTableContainer.allowedChildren.push(TableHeader)
TableHeader.requiredContainer = MyTableContainer


class CustomTable extends Quill.import('modules/table'){
    // We need to register a new sub containers here
    static register() {
        Quill.register(MyTableRow);
        Quill.register(TableHeaderCell);
        Quill.register(TableHeader);
        Quill.register(MyTableContainer);
    }
    
    static handler(value){
        const table = quill.getModule('table');
        if (value){
            table.insertTable(1,1)
            let tooltip = new TableTooltip(quill, table.getTable()[0], '')
            //tooltip.setHeight(document.querySelector('footer').getBoundingClientRect().height)
            tooltip.setHeight(48)
            tooltip.show()
        }else{
            TableTooltip.remove()
            table.deleteTable()
        }
    }


    insertHeader(offset) {
        const range = this.quill.getSelection();
        if (!range) return;
        const [table, row, cell] = this.getTable(range);
        if (cell == null) return;
        const index = row.rowOffset();
        table.insertHeaderRow();
        this.quill.update(Quill.sources.USER);
        if (offset > 0) {
          this.quill.setSelection(range, Quill.sources.SILENT);
        } else {
          this.quill.setSelection(
            range.index + row.children.length,
            range.length,
            Quill.sources.SILENT,
          );
        }
    }

    deleteHeader() {
        const range = this.quill.getSelection();
        if (!range) return;
        const [table, row, cell] = this.getTable(range);
        if (cell == null) return;
        table.deleteHeaderRow();
        this.quill.update(Quill.sources.USER);
    }
    // This is modified method to work with headers
    insertColumn(offset) {
        const range = this.quill.getSelection();
        if (!range) return;
        const [table, row, cell] = this.getTable(range);
        if (cell == null) return;
        const column = cell.cellOffset();
        table.insertColumn(column + offset);
        table.insertHeaderColumn(column + offset);
        this.quill.update(Quill.sources.USER);
        let shift = row.rowOffset();
        if (offset === 0) {
          shift += 1;
        }
        this.quill.setSelection(
          range.index + shift,
          range.length,
          Quill.sources.SILENT,
        );
    }
    // This is modified method to work with headers
    deleteColumn() {
        const [table, , cell] = this.getTable();
        if (cell == null) return;
        // @ts-expect-error
        table.deleteColumn(cell.cellOffset());
        table.deleteHeaderColumn(cell.cellOffset());
        this.quill.update(Quill.sources.USER);
    }
    
    deleteRow() {
        const [, row] = this.getTable();
        if (row == null) return;
        row.remove();
        this.quill.update(Quill.sources.USER);
    }

    listenBalanceCells() {
        this.quill.on(
          Quill.events.SCROLL_OPTIMIZE,
          (mutations) => {
            mutations.some((mutation) => {
              if (
                ['TH', 'TD', 'TR', 'THEAD', 'TBODY', 'TABLE'].includes(
                  mutation.target.tagName,
                )
              ) {
                this.quill.once(Quill.events.TEXT_CHANGE, (delta, old, source) => {
                  if (source !== Quill.sources.USER) return;
                  this.balanceTables();
                });
                return true;
              }
              return false;
            });
          },
        );
    }
}

Quill.register('modules/table', CustomTable, true);